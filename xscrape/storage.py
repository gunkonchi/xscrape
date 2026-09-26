"""Storage backends."""

from __future__ import annotations
import csv
import json
import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path

from .models import Tweet


class BaseStorage(ABC):
    @abstractmethod
    async def save(self, tweets: list[Tweet]) -> None: ...


class JsonStorage(BaseStorage):
    def __init__(self, path: str | Path):
        self.path = Path(path)

    async def save(self, tweets: list[Tweet]) -> None:
        self.path.write_text(
            json.dumps([t.to_dict() for t in tweets], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


class CsvStorage(BaseStorage):
    FIELDS = ["id", "created_at", "author", "text", "likes", "retweets", "replies"]

    def __init__(self, path: str | Path):
        self.path = Path(path)

    async def save(self, tweets: list[Tweet]) -> None:
        with self.path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDS)
            writer.writeheader()
            for t in tweets:
                writer.writerow({
                    "id": t.id,
                    "created_at": t.created_at.isoformat() if t.created_at else "",
                    "author": t.author.username,
                    "text": t.text.replace("\n", " "),
                    "likes": t.likes,
                    "retweets": t.retweets,
                    "replies": t.replies,
                })


class SqliteStorage(BaseStorage):
    def __init__(self, path: str | Path):
        self.path = Path(path)

    async def save(self, tweets: list[Tweet]) -> None:
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
