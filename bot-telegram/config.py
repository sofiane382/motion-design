"""Lecture des réglages depuis le fichier .env (ou les variables d'environnement)."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


def _int(name: str, default: int) -> int:
    value = os.getenv(name, "").strip()
    return int(value) if value else default


def _float(name: str, default: float) -> float:
    value = os.getenv(name, "").strip()
    return float(value) if value else default


@dataclass
class Config:
    token: str = ""
    admin_user_id: int | None = None
    max_photos_per_hour: int = 20
    max_photos_per_day: int = 60
    max_photos_per_album: int = 10
    max_file_size_mb: int = 15
    max_concurrent_jobs: int = 2
    processing_timeout: float = 60
    spam_max_messages: int = 5
    spam_window: float = 10
    spam_mute: float = 60
    group_max_per_minute: int = 20
    album_send_pause: float = 1
    stats_db_path: str = "stats.db"
    webhook_url: str = ""
    port: int = 10000

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024

    @classmethod
    def from_env(cls) -> "Config":
        load_dotenv()
        admin = os.getenv("ADMIN_USER_ID", "").strip()
        return cls(
            token=os.getenv("TELEGRAM_BOT_TOKEN", "").strip(),
            admin_user_id=int(admin) if admin else None,
            max_photos_per_hour=_int("MAX_PHOTOS_PER_HOUR", 20),
            max_photos_per_day=_int("MAX_PHOTOS_PER_DAY", 60),
            max_photos_per_album=_int("MAX_PHOTOS_PER_ALBUM", 10),
            max_file_size_mb=_int("MAX_FILE_SIZE_MB", 15),
            max_concurrent_jobs=_int("MAX_CONCURRENT_JOBS", 2),
            processing_timeout=_float("PROCESSING_TIMEOUT_SECONDS", 60),
            spam_max_messages=_int("SPAM_MAX_MESSAGES", 5),
            spam_window=_float("SPAM_WINDOW_SECONDS", 10),
            spam_mute=_float("SPAM_MUTE_SECONDS", 60),
            group_max_per_minute=_int("GROUP_MAX_MESSAGES_PER_MINUTE", 20),
            album_send_pause=_float("ALBUM_SEND_PAUSE_SECONDS", 1),
            stats_db_path=os.getenv("STATS_DB_PATH", "stats.db").strip() or "stats.db",
            webhook_url=(os.getenv("WEBHOOK_URL", "").strip()
                         or os.getenv("RENDER_EXTERNAL_URL", "").strip()),
            port=_int("PORT", 10000),
        )
