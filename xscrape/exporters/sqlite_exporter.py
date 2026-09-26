"""SQLite exporter."""

import sqlite3
from .base import BaseExporter
from ..models import Tweet


class SqliteExporter(BaseExporter):
    extension = ".db"

    async def export(self, tweets: list[Tweet]) -> None:
        conn = sqlite3.connect(self.path)
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tweets (
                    id TEXT PRIMARY KEY,
                    created_at TEXT,
                    author TEXT,
                    text TEXT,
                    likes INTEGER,
                    retweets INTEGER,
                    replies INTEGER
                )
                """
            )
            conn.executemany(
                "INSERT OR REPLACE INTO tweets VALUES (?, ?, ?, ?, ?, ?, ?)",
                [
                    (
                        t.id,
                        t.created_at.isoformat() if t.created_at else None,
                        t.author.username,
                        t.text,
                        t.likes,
                        t.retweets,
                        t.replies,
                    )
                    for t in tweets
                ],
            )
            conn.commit()
        finally:
            conn.close()
