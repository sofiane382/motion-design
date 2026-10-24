"""Bot Telegram public qui rend les photos de produits plus propres pour la vente.

Lancement : python bot.py (réglages dans le fichier .env)
"""

import asyncio
import gc
import hashlib
import io
import logging
import time

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from config import Config
from limits import ChatThrottle, ProcessingQueue, SpamGuard, UserRateLimiter, format_delay
from processor import HEIC_SUPPORTED, NotAnImageError, process_image
from stats import Stats

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)
# httpx écrit les adresses appelées, qui contiennent le token : on le fait taire
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("bot")

ACCEPTED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"}
ACCEPTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif")

START_TEXT = (
    "📸 Envoie-moi une photo de ton produit : je la rends plus lumineuse, plus nette "
    "et je la mets en format carré sur fond blanc, prête pour ton annonce.\n"
    "Tu peux envoyer une photo ou un album (10 max), en photo ou en fichier.\n"
    "Commandes : /confidentialite et /conditions.\n"
    "Utilise uniquement tes propres photos. Aucune photo n'est conservée : "
    "tout est supprimé juste après l'envoi."
)

PRIVACY_TEXT = (
    "🔒 Confidentialité\n\n"
    "• Tes photos sont traitées en mémoire puis effacées dès que le résultat t'est envoyé. "
    "Elles ne sont jamais enregistrées, ni sur disque, ni ailleurs.\n"
    "• Les métadonnées de tes photos (position GPS, modèle de téléphone...) sont retirées "
    "du résultat.\n"
    "• Aucun message, nom ou numéro n'est conservé.\n"
    "• Le bot garde seulement des compteurs anonymes : nombre de photos traitées, nombre "
    "d'erreurs et nombre d'utilisateurs différents (sous forme d'empreinte chiffrée "
    "impossible à relier à ton compte)."
)

TERMS_TEXT = (
    "📄 Conditions d'utilisation\n\n"
    "Tu es responsable des photos que tu envoies. N'envoie que des photos dont tu es "
    "l'auteur ou dont tu as les droits. Le bot ne doit pas servir à reprendre les photos "
    "de quelqu'un d'autre ou à tromper des acheteurs."
)

NOT_AN_IMAGE_TEXT = (
    "Désolé, je ne sais traiter que les images JPEG, PNG, WEBP"
    + (" et HEIC" if HEIC_SUPPORTED else "")
    + ". Ce fichier n'en est pas une 🙂"
)


class AlbumTracker:
    """Se souvient brièvement des albums en cours (compteur de photos, messages déjà envoyés)."""

    def __init__(self, ttl: float = 600, clock=time.monotonic):
        self.ttl = ttl
        self.clock = clock
        self._albums: dict[str, dict] = {}

    def get(self, group_id: str) -> dict:
        now = self.clock()
        for key in [k for k, v in self._albums.items() if v["seen"] < now - self.ttl]:
            del self._albums[key]
        album = self._albums.setdefault(group_id, {"count": 0, "notices": set(), "seen": now})
        album["seen"] = now
        return album


class PhotoBot:
    def __init__(self, config: Config, stats: Stats | None = None, clock=time.monotonic,
                 sleep=asyncio.sleep):
        self.config = config
        self.sleep = sleep
        salt = hashlib.sha256(("stats:" + config.token).encode()).hexdigest()
        self.stats = stats or Stats(config.stats_db_path, salt)
        self.rate_limiter = UserRateLimiter(config.max_photos_per_hour, config.max_photos_per_day, clock)
        self.spam = SpamGuard(config.spam_max_messages, config.spam_window, config.spam_mute, clock)
        self.queue = ProcessingQueue(config.max_concurrent_jobs)
        self.throttle = ChatThrottle(config.group_max_per_minute, clock, sleep)
        self.albums = AlbumTracker(clock=clock)

    # ---------- outils ----------

    async def _reply(self, update: Update, text: str) -> None:
        chat = update.effective_chat
        await self.throttle.wait(chat.id, chat.type != ChatType.PRIVATE)
        await update.effective_message.reply_text(text)

    async def _spam_check(self, update: Update) -> bool:
        """True si le message doit être traité, False s'il faut l'ignorer."""
        user = update.effective_user
        message = update.effective_message
        if user is None or message is None:
            return False
        group_id = message.media_group_id
        if group_id:
            # Un album compte pour un seul message
            album = self.albums.get(group_id)
            if album.get("spam_status") is None:
                album["spam_status"] = self.spam.register(user.id)
            status = album["spam_status"]
        else:
            status = self.spam.register(user.id)
        if status == "just_muted" and (not group_id or "spam" not in album["notices"]):
            if group_id:
                album["notices"].add("spam")
            await self._reply(update, f"⏸️ Trop de messages d'un coup. Je t'ignore pendant "
                                      f"{format_delay(self.config.spam_mute)}, puis tu pourras reprendre.")
        return status == "ok"

    # ---------- commandes ----------

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if await self._spam_check(update):
            await self._reply(update, START_TEXT)

    async def privacy(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if await self._spam_check(update):
            await self._reply(update, PRIVACY_TEXT)

    async def terms(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if await self._spam_check(update):
            await self._reply(update, TERMS_TEXT)

    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not await self._spam_check(update):
            return
        admin = self.config.admin_user_id
        if admin is None or update.effective_user.id != admin:
            await self._reply(update, "Cette commande est réservée à l'administrateur du bot.")
            return
        s = await asyncio.to_thread(self.stats.summary)
        await self._reply(update, (
            "📊 Statistiques\n"
            f"Utilisateurs différents : {s['users']}\n"
            f"Photos traitées aujourd'hui : {s['photos_today']}\n"
            f"Photos traitées au total : {s['photos_total']}\n"
            f"Erreurs : {s['errors']}\n"
            f"En cours : {self.queue.running} · En attente : {self.queue.waiting}"
        ))

    async def other_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not await self._spam_check(update):
            return
        if update.effective_chat.type == ChatType.PRIVATE:
            await self._reply(update, "Envoie-moi une photo (JPEG, PNG, WEBP ou HEIC) 📸 "
                                      "Tape /start pour l'aide.")

    # ---------- photos ----------

    async def media(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not await self._spam_check(update):
            return
        message = update.effective_message
        user_id = update.effective_user.id
        group_id = message.media_group_id
        album = self.albums.get(group_id) if group_id else None

        async def notice_once(key: str, text: str) -> None:
            if album is None:
                await self._reply(update, text)
            elif key not in album["notices"]:
                album["notices"].add(key)
                await self._reply(update, text)

        if album is not None:
            album["count"] += 1
            if album["count"] > self.config.max_photos_per_album:
                await notice_once("album", f"Maximum {self.config.max_photos_per_album} photos par "
                                           "album : les suivantes sont ignorées.")
                return

        if message.photo:
            file = message.photo[-1]
        elif message.document:
            doc = message.document
            name = (doc.file_name or "").lower()
            if doc.mime_type not in ACCEPTED_MIME_TYPES and not name.endswith(ACCEPTED_EXTENSIONS):
                await notice_once("type", NOT_AN_IMAGE_TEXT)
                return
            file = doc
        else:
            return

        if file.file_size and file.file_size > self.config.max_file_size_bytes:
            await notice_once("size", f"Ce fichier est trop lourd : {self.config.max_file_size_mb} Mo "
                                      "maximum par photo.")
            return

        allowed, wait, period = self.rate_limiter.try_consume(user_id)
        if not allowed:
            limit = self.config.max_photos_per_hour if period == "heure" else self.config.max_photos_per_day
            await notice_once("quota", f"⏳ Tu as atteint la limite de {limit} photos par {period}. "
                                       f"Tu pourras réessayer dans {format_delay(wait)}.")
            return

        await asyncio.to_thread(self.stats.record_user, user_id)

        position = self.queue.position_if_queued()
        if position:
            await self._reply(update, f"🕐 Tu es en position {position} dans la file, ta photo arrive.")

        result = await self._process(update, context, file, user_id)
        if result is None:
            return
        try:
            if group_id:
                await self.sleep(self.config.album_send_pause)
            chat = update.effective_chat
            await self.throttle.wait(chat.id, chat.type != ChatType.PRIVATE)
            await message.reply_document(document=io.BytesIO(result), filename="photo_pro.jpg")
            await asyncio.to_thread(self.stats.record_photo)
        except Exception:
            log.exception("Envoi du résultat impossible")
            await asyncio.to_thread(self.stats.record_error)
        finally:
            del result
            gc.collect()

    async def _process(self, update: Update, context, file, user_id: int) -> bytes | None:
        """Télécharge et traite la photo dans la file d'attente. None en cas d'échec."""
        async with self.queue:
            data = None
            task = None
            try:
                tg_file = await file.get_file()
                data = bytes(await tg_file.download_as_bytearray())
                task = asyncio.create_task(asyncio.to_thread(process_image, data))
                return await asyncio.wait_for(asyncio.shield(task), self.config.processing_timeout)
            except NotAnImageError:
                self.rate_limiter.refund(user_id)
                await self._reply(update, NOT_AN_IMAGE_TEXT)
            except asyncio.TimeoutError:
                await asyncio.to_thread(self.stats.record_error)
                await self._reply(update, "😕 Cette photo a pris trop de temps à traiter. "
                                          "Essaie avec une image plus petite.")
                # On attend la fin du calcul avant de libérer la place dans la file
                try:
                    await task
                except Exception:
                    pass
            except Exception:
                log.exception("Erreur pendant le traitement d'une photo")
                await asyncio.to_thread(self.stats.record_error)
                await self._reply(update, "😕 Oups, je n'ai pas réussi à traiter cette photo. "
                                          "Réessaie dans un instant.")
            finally:
                del data
                gc.collect()
        return None

    # ---------- démarrage ----------

    def build_application(self) -> Application:
        app = (Application.builder().token(self.config.token)
               .concurrent_updates(True).build())
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("aide", self.start))
        app.add_handler(CommandHandler("help", self.start))
        app.add_handler(CommandHandler("confidentialite", self.privacy))
        app.add_handler(CommandHandler("conditions", self.terms))
        app.add_handler(CommandHandler("stats", self.show_stats))
        app.add_handler(MessageHandler(filters.PHOTO | filters.Document.ALL, self.media))
        app.add_handler(MessageHandler(~filters.COMMAND & ~filters.StatusUpdate.ALL, self.other_message))
        app.add_error_handler(self._on_error)
        return app

    async def _on_error(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        log.error("Erreur non gérée : %s", context.error)


def main() -> None:
    config = Config.from_env()
    if not config.token:
        raise SystemExit("TELEGRAM_BOT_TOKEN manquant : ajoute-le dans le fichier .env")
    bot = PhotoBot(config)
    log.info("Bot démarré (public). Admin configuré : %s", "oui" if config.admin_user_id else "non")
    bot.build_application().run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
