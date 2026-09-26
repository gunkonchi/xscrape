"""Base plugin class."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class PluginContext:
    endpoint: str
    params: dict
    status: Optional[int] = None
    duration_ms: Optional[float] = None
    payload: Any = None


class Plugin:
    """Base class for xscrape plugins."""

    name: str = "plugin"

    async def on_start(self) -> None: ...
    async def on_request(self, ctx: PluginContext) -> None: ...
    async def on_response(self, ctx: PluginContext) -> None: ...
    async def on_parse(self, ctx: PluginContext) -> None: ...
    async def on_save(self, ctx: PluginContext) -> None: ...
    async def on_stop(self) -> None: ...
