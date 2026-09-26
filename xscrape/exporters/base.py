"""Base exporter interface."""

from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path

from ..models import Tweet


class BaseExporter(ABC):
    extension: str = ""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    @abstractmethod
    async def export(self, tweets: list[Tweet]) -> None: ...
