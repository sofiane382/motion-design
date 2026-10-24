"""Statistiques anonymes dans un petit fichier SQLite.

Ne contient que des compteurs et des empreintes (hash) d'identifiants :
jamais de photo, de nom, de message ni d'identifiant Telegram en clair.
"""

import hashlib
import sqlite3
import threading
from datetime import date


class Stats:
    def __init__(self, path: str, salt: str):
        self._salt = salt.encode()
        self._lock = threading.Lock()
        self._db = sqlite3.connect(path, check_same_thread=False)
        with self._db:
            self._db.execute("CREATE TABLE IF NOT EXISTS users (hash TEXT PRIMARY KEY)")
            self._db.execute(
                "CREATE TABLE IF NOT EXISTS daily ("
                "day TEXT PRIMARY KEY, photos INTEGER NOT NULL DEFAULT 0, "
                "errors INTEGER NOT NULL DEFAULT 0)"
            )

    def _hash(self, user_id: int) -> str:
        return hashlib.sha256(self._salt + str(user_id).encode()).hexdigest()

    def _bump(self, column: str) -> None:
        today = date.today().isoformat()
        with self._lock, self._db:
            self._db.execute("INSERT OR IGNORE INTO daily (day) VALUES (?)", (today,))
            self._db.execute(f"UPDATE daily SET {column} = {column} + 1 WHERE day = ?", (today,))

    def record_user(self, user_id: int) -> None:
        with self._lock, self._db:
            self._db.execute("INSERT OR IGNORE INTO users (hash) VALUES (?)", (self._hash(user_id),))

    def record_photo(self) -> None:
        self._bump("photos")

    def record_error(self) -> None:
        self._bump("errors")

    def summary(self) -> dict[str, int]:
        today = date.today().isoformat()
        with self._lock:
            users = self._db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            photos_today = self._db.execute(
                "SELECT COALESCE(SUM(photos), 0) FROM daily WHERE day = ?", (today,)
            ).fetchone()[0]
            photos_total, errors = self._db.execute(
                "SELECT COALESCE(SUM(photos), 0), COALESCE(SUM(errors), 0) FROM daily"
            ).fetchone()
        return {"users": users, "photos_today": photos_today,
                "photos_total": photos_total, "errors": errors}

    def close(self) -> None:
        self._db.close()
