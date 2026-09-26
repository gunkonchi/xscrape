"""CSV exporter."""

import csv
from .base import BaseExporter
from ..models import Tweet


class CsvExporter(BaseExporter):
    extension = ".csv"
    FIELDS = ["id", "created_at", "author", "text", "likes", "retweets", "replies"]

    async def export(self, tweets: list[Tweet]) -> None:
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
