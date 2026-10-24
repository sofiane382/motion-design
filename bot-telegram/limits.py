"""Protections contre les abus : quotas, anti-spam, file d'attente, rythme d'envoi."""

import asyncio
import time
from collections import defaultdict, deque
from typing import Callable

HOUR = 3600
DAY = 86400


class UserRateLimiter:
    """Quota de photos par utilisateur sur une heure et sur 24 heures glissantes."""

    def __init__(self, per_hour: int, per_day: int, clock: Callable[[], float] = time.monotonic):
        self.per_hour = per_hour
        self.per_day = per_day
        self.clock = clock
        self._history: dict[int, deque[float]] = defaultdict(deque)

    def try_consume(self, user_id: int) -> tuple[bool, float, str]:
        """Réserve une photo. Renvoie (autorisé, secondes à attendre, 'heure'|'jour')."""
        now = self.clock()
        history = self._history[user_id]
        while history and history[0] <= now - DAY:
            history.popleft()

        if len(history) >= self.per_day:
            return False, history[-self.per_day] + DAY - now, "jour"

        last_hour = [t for t in history if t > now - HOUR]
        if len(last_hour) >= self.per_hour:
            return False, last_hour[-self.per_hour] + HOUR - now, "heure"

        history.append(now)
        return True, 0.0, ""

    def refund(self, user_id: int) -> None:
        """Rend une photo qui n'a finalement pas été traitée (fichier refusé...)."""
        history = self._history.get(user_id)
        if history:
            history.pop()


class SpamGuard:
    """Ignore un utilisateur qui envoie trop de messages trop vite."""

    def __init__(self, max_messages: int, window: float, mute: float,
                 clock: Callable[[], float] = time.monotonic):
        self.max_messages = max_messages
        self.window = window
        self.mute = mute
        self.clock = clock
        self._messages: dict[int, deque[float]] = defaultdict(deque)
        self._muted_until: dict[int, float] = {}

    def is_muted(self, user_id: int) -> bool:
        return self._muted_until.get(user_id, 0) > self.clock()

    def register(self, user_id: int) -> str:
        """Compte un message. Renvoie 'ok', 'just_muted' (vient d'être bloqué) ou 'muted'."""
        now = self.clock()
        if self.is_muted(user_id):
            return "muted"
        messages = self._messages[user_id]
        messages.append(now)
        while messages and messages[0] <= now - self.window:
            messages.popleft()
        if len(messages) > self.max_messages:
            self._muted_until[user_id] = now + self.mute
            messages.clear()
            return "just_muted"
        return "ok"


class ProcessingQueue:
    """File d'attente globale : au plus N traitements en même temps."""

    def __init__(self, max_concurrent: int):
        self.max_concurrent = max_concurrent
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self.running = 0
        self.waiting = 0

    def position_if_queued(self) -> int:
        """0 si un emplacement est libre, sinon la position qu'aurait un nouvel arrivant."""
        if self.running + self.waiting < self.max_concurrent:
            return 0
        return self.waiting + 1

    async def __aenter__(self):
        self.waiting += 1
        try:
            await self._semaphore.acquire()
        finally:
            self.waiting -= 1
        self.running += 1
        return self

    async def __aexit__(self, *exc):
        self.running -= 1
        self._semaphore.release()
        return False


class ChatThrottle:
    """Évite de dépasser la limite d'envoi de Telegram dans un même groupe."""

    def __init__(self, group_per_minute: int, clock: Callable[[], float] = time.monotonic,
                 sleep=asyncio.sleep):
        self.group_per_minute = group_per_minute
        self.clock = clock
        self.sleep = sleep
        self._sent: dict[int, deque[float]] = defaultdict(deque)
        self._locks: dict[int, asyncio.Lock] = defaultdict(asyncio.Lock)

    async def wait(self, chat_id: int, is_group: bool) -> None:
        if not is_group:
            return
        async with self._locks[chat_id]:
            sent = self._sent[chat_id]
            while True:
                now = self.clock()
                while sent and sent[0] <= now - 60:
                    sent.popleft()
                if len(sent) < self.group_per_minute:
                    sent.append(now)
                    return
                await self.sleep(sent[0] + 60 - now + 0.05)


def format_delay(seconds: float) -> str:
    """Transforme un nombre de secondes en texte lisible : '12 min', '1 h 05'."""
    minutes = max(1, int(seconds // 60) + (1 if seconds % 60 else 0))
    if minutes < 60:
        return f"{minutes} min"
    hours, rest = divmod(minutes, 60)
    return f"{hours} h {rest:02d}" if rest else f"{hours} h"
