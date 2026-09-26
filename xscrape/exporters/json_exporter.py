"""JSON exporter."""

import json
from .base import BaseExporter
from ..models import Tweet


class JsonExporter(BaseExporter):
    extension = ".json"

    async def export(self, tweets: list[Tweet]) -> None:
        self.path.write_text(
            json.dumps([t.to_dict() for t in tweets], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
