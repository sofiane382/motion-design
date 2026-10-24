import asyncio
import io
from unittest.mock import AsyncMock, MagicMock

from PIL import Image
from telegram.constants import ChatType

import bot as bot_module
from bot import PhotoBot
from config import Config
from limits import ChatThrottle, ProcessingQueue, SpamGuard, UserRateLimiter, format_delay
from stats import Stats

ADMIN = 111
USER = 222


class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


def jpeg_bytes():
    out = io.BytesIO()
    Image.new("RGB", (100, 80), "blue").save(out, "JPEG")
    return out.getvalue()


def make_bot(tmp_path, clock=None, **overrides):
    config = Config(token="test", admin_user_id=ADMIN, stats_db_path=str(tmp_path / "stats.db"),
                    album_send_pause=0, **overrides)
    return PhotoBot(config, clock=clock or FakeClock(), sleep=AsyncMock())


def make_update(user_id=USER, photo_data=None, document=None, group_id=None, chat_type=ChatType.PRIVATE):
    update = MagicMock()
    update.effective_user.id = user_id
    update.effective_chat.id = user_id
    update.effective_chat.type = chat_type
    message = update.effective_message
    message.reply_text = AsyncMock()
    message.reply_document = AsyncMock()
    message.media_group_id = group_id
    message.document = document
    message.photo = []
    if photo_data is not None:
        size = MagicMock(file_size=len(photo_data))
        tg_file = MagicMock()
        tg_file.download_as_bytearray = AsyncMock(return_value=bytearray(photo_data))
        size.get_file = AsyncMock(return_value=tg_file)
        message.photo = [size]
    return update


def make_document(data, mime, name, size=None):
    doc = MagicMock(mime_type=mime, file_name=name, file_size=size if size is not None else len(data))
    tg_file = MagicMock()
    tg_file.download_as_bytearray = AsyncMock(return_value=bytearray(data))
    doc.get_file = AsyncMock(return_value=tg_file)
    return doc


def replies(update):
    return [c.args[0] for c in update.effective_message.reply_text.call_args_list]


# ---------- limite par utilisateur ----------

def test_rate_limit_per_hour_and_day():
    clock = FakeClock()
    limiter = UserRateLimiter(per_hour=20, per_day=60, clock=clock)
    for _ in range(20):
        assert limiter.try_consume(USER)[0]
    allowed, wait, period = limiter.try_consume(USER)
    assert not allowed and period == "heure" and 0 < wait <= 3600
    assert limiter.try_consume(ADMIN)[0]  # les autres ne sont pas touchés

    for _ in range(2):
        clock.now += 3601
        for _ in range(20):
            assert limiter.try_consume(USER)[0]
    clock.now += 3601
    allowed, wait, period = limiter.try_consume(USER)
    assert not allowed and period == "jour"
    clock.now += 86400
    assert limiter.try_consume(USER)[0]


def test_rate_limit_message_says_when_to_retry(tmp_path):
    bot = make_bot(tmp_path, max_photos_per_hour=2)

    async def run():
        for _ in range(3):
            update = make_update(photo_data=jpeg_bytes())
            await bot.media(update, None)
        return update

    update = asyncio.run(run())
    assert any("limite de 2 photos par heure" in r and "réessayer dans 1 h" in r for r in replies(update))
    update.effective_message.reply_document.assert_not_called()


def test_format_delay():
    assert format_delay(30) == "1 min"
    assert format_delay(600) == "10 min"
    assert format_delay(3900) == "1 h 05"


# ---------- file d'attente ----------

def test_queue_limits_concurrency_and_reports_position():
    async def run():
        queue = ProcessingQueue(2)
        active, peak = 0, 0
        positions = []
        release = asyncio.Event()

        async def job():
            nonlocal active, peak
            positions.append(queue.position_if_queued())
            async with queue:
                active += 1
                peak = max(peak, active)
                await release.wait()
                active -= 1

        tasks = []
        for _ in range(5):
            tasks.append(asyncio.create_task(job()))
            await asyncio.sleep(0)
        assert queue.running == 2 and queue.waiting == 3
        release.set()
        await asyncio.gather(*tasks)
        return peak, positions

    peak, positions = asyncio.run(run())
    assert peak == 2
    assert positions == [0, 0, 1, 2, 3]


def test_processing_runs_in_thread_and_does_not_block(tmp_path, monkeypatch):
    """Pendant qu'une photo lente est traitée, le bot répond toujours aux autres."""
    import time

    def slow(data):
        time.sleep(0.5)
        return b"ok"

    monkeypatch.setattr(bot_module, "process_image", slow)
    bot = make_bot(tmp_path)

    async def run():
        slow_task = asyncio.create_task(bot.media(make_update(photo_data=jpeg_bytes()), None))
        await asyncio.sleep(0.05)
        other = make_update(user_id=333)
        started = asyncio.get_running_loop().time()
        await bot.start(other, None)
        elapsed = asyncio.get_running_loop().time() - started
        await slow_task
        return elapsed, other

    elapsed, other = asyncio.run(run())
    assert elapsed < 0.2
    assert "Envoie-moi une photo" in replies(other)[0]


def test_timeout_gives_clean_error(tmp_path, monkeypatch):
    import time
    monkeypatch.setattr(bot_module, "process_image", lambda data: time.sleep(0.3) or b"ok")
    bot = make_bot(tmp_path, processing_timeout=0.05)
    update = make_update(photo_data=jpeg_bytes())
    asyncio.run(bot.media(update, None))
    assert any("trop de temps" in r for r in replies(update))
    update.effective_message.reply_document.assert_not_called()
    assert bot.stats.summary()["errors"] == 1
    assert bot.queue.running == 0


def test_queue_position_message(tmp_path):
    bot = make_bot(tmp_path)
    bot.queue.running = 2  # deux photos déjà en cours
    bot.queue._semaphore = asyncio.Semaphore(2)
    update = make_update(photo_data=jpeg_bytes())
    asyncio.run(bot.media(update, None))
    assert any("position 1 dans la file" in r for r in replies(update))


# ---------- anti-spam ----------

def test_spam_guard_mutes_for_one_minute():
    clock = FakeClock()
    guard = SpamGuard(max_messages=5, window=10, mute=60, clock=clock)
    assert [guard.register(USER) for _ in range(5)] == ["ok"] * 5
    assert guard.register(USER) == "just_muted"
    clock.now += 30
    assert guard.register(USER) == "muted"
    clock.now += 31
    assert guard.register(USER) == "ok"


def test_spam_messages_are_ignored_by_bot(tmp_path):
    bot = make_bot(tmp_path)
    update = make_update()

    async def run():
        for _ in range(10):
            await bot.start(update, None)

    asyncio.run(run())
    texts = replies(update)
    assert len(texts) == 6  # 5 réponses normales + 1 avertissement, puis plus rien
    assert "Je t'ignore pendant 1 min" in texts[-1]


def test_album_counts_as_one_message_for_spam_and_max_10(tmp_path):
    bot = make_bot(tmp_path)

    async def run():
        updates = [make_update(photo_data=jpeg_bytes(), group_id="album1") for _ in range(12)]
        for u in updates:
            await bot.media(u, None)
        return updates

    updates = asyncio.run(run())
    sent = sum(u.effective_message.reply_document.call_count for u in updates)
    assert sent == 10
    all_replies = [r for u in updates for r in replies(u)]
    assert sum("Maximum 10 photos par album" in r for r in all_replies) == 1
    assert not any("ignore" in r.lower() and "pendant" in r for r in all_replies)


def test_group_throttle_waits():
    clock = FakeClock()
    sleeps = []

    async def fake_sleep(s):
        sleeps.append(s)
        clock.now += s

    throttle = ChatThrottle(group_per_minute=20, clock=clock, sleep=fake_sleep)

    async def run():
        for _ in range(21):
            await throttle.wait(-100, is_group=True)
        for _ in range(50):
            await throttle.wait(5, is_group=False)

    asyncio.run(run())
    assert len(sleeps) == 1 and sleeps[0] > 59


# ---------- refus des non-images ----------

def test_rejects_non_image_document(tmp_path):
    bot = make_bot(tmp_path)
    update = make_update(document=make_document(b"%PDF-1.4", "application/pdf", "facture.pdf"))
    asyncio.run(bot.media(update, None))
    assert "ne sais traiter que les images" in replies(update)[0]
    update.effective_message.reply_document.assert_not_called()


def test_rejects_fake_image_with_image_extension(tmp_path):
    bot = make_bot(tmp_path)
    update = make_update(document=make_document(b"pas une image", "image/jpeg", "piege.jpg"))
    asyncio.run(bot.media(update, None))
    assert any("ne sais traiter que les images" in r for r in replies(update))
    update.effective_message.reply_document.assert_not_called()
    # la tentative ratée ne compte pas dans le quota
    assert len(bot.rate_limiter._history[USER]) == 0


def test_rejects_file_over_15_mb(tmp_path):
    bot = make_bot(tmp_path)
    doc = make_document(jpeg_bytes(), "image/jpeg", "grosse.jpg", size=16 * 1024 * 1024)
    update = make_update(document=doc)
    asyncio.run(bot.media(update, None))
    assert "15 Mo" in replies(update)[0]
    doc.get_file.assert_not_called()


def test_accepts_image_document_and_photo(tmp_path):
    bot = make_bot(tmp_path)
    u1 = make_update(document=make_document(jpeg_bytes(), "image/jpeg", "produit.jpg"))
    u2 = make_update(photo_data=jpeg_bytes())

    async def run():
        await bot.media(u1, None)
        await bot.media(u2, None)

    asyncio.run(run())
    u1.effective_message.reply_document.assert_called_once()
    u2.effective_message.reply_document.assert_called_once()


# ---------- /stats ----------

def test_stats_only_for_admin(tmp_path):
    bot = make_bot(tmp_path)
    asyncio.run(bot.media(make_update(photo_data=jpeg_bytes()), None))

    user_update = make_update(user_id=USER)
    asyncio.run(bot.show_stats(user_update, None))
    assert "réservée à l'administrateur" in replies(user_update)[0]

    admin_update = make_update(user_id=ADMIN)
    asyncio.run(bot.show_stats(admin_update, None))
    text = replies(admin_update)[0]
    assert "Utilisateurs différents : 1" in text
    assert "aujourd'hui : 1" in text and "au total : 1" in text and "Erreurs : 0" in text


def test_stats_refused_when_no_admin_configured(tmp_path):
    bot = make_bot(tmp_path)
    bot.config.admin_user_id = None
    update = make_update(user_id=ADMIN)
    asyncio.run(bot.show_stats(update, None))
    assert "réservée" in replies(update)[0]


def test_stats_db_stores_no_raw_ids(tmp_path):
    path = tmp_path / "s.db"
    stats = Stats(str(path), salt="sel")
    stats.record_user(123456789)
    stats.record_user(123456789)
    stats.record_photo()
    stats.record_error()
    assert stats.summary() == {"users": 1, "photos_today": 1, "photos_total": 1, "errors": 1}
    stats.close()
    assert b"123456789" not in path.read_bytes()


def test_my_id_command(tmp_path):
    bot = make_bot(tmp_path)
    update = make_update(user_id=4242)
    asyncio.run(bot.my_id(update, None))
    assert "4242" in replies(update)[0]


def test_bot_sets_its_own_menu_and_description(tmp_path):
    bot = make_bot(tmp_path)
    app = MagicMock()
    app.bot.set_my_commands = AsyncMock()
    app.bot.set_my_short_description = AsyncMock()
    app.bot.set_my_description = AsyncMock(side_effect=RuntimeError("réseau"))  # ne doit pas planter
    asyncio.run(bot.setup_profile(app))
    names = [c.command for c in app.bot.set_my_commands.call_args.args[0]]
    assert "stats" not in names and "start" in names


def test_webhook_mode_only_when_url_known():
    from bot import webhook_settings
    assert webhook_settings(Config(token="t")) is None
    settings = webhook_settings(Config(token="t", webhook_url="https://bot.onrender.com/", port=8080))
    assert settings["webhook_url"] == "https://bot.onrender.com/telegram"
    assert settings["port"] == 8080 and settings["secret_token"]
    assert "drop_pending_updates" not in settings


def test_render_url_is_detected(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "t")
    monkeypatch.delenv("WEBHOOK_URL", raising=False)
    monkeypatch.setenv("RENDER_EXTERNAL_URL", "https://x.onrender.com")
    monkeypatch.setenv("PORT", "1234")
    config = Config.from_env()
    assert config.webhook_url == "https://x.onrender.com" and config.port == 1234


def test_pasted_command_without_command_formatting_still_works(tmp_path):
    bot = make_bot(tmp_path)
    update = make_update(user_id=4242)
    update.effective_message.text = "/monid"
    asyncio.run(bot.other_message(update, None))
    assert "4242" in replies(update)[0]

    update = make_update()
    update.effective_message.text = "bonjour"
    asyncio.run(bot.other_message(update, None))
    assert "Envoie-moi une photo" in replies(update)[0]
