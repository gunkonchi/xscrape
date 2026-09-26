"""Plugin registry."""

from __future__ import annotations
import importlib
from typing import Iterable

from .base import Plugin


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: list[Plugin] = []

    def register(self, plugin: Plugin) -> None:
        self._plugins.append(plugin)

    def register_many(self, plugins: Iterable[Plugin]) -> None:
        for p in plugins:
            self.register(p)

    def load(self, dotted_path: str) -> None:
        """Load a plugin from `module.path:ClassName`."""
        module_path, _, class_name = dotted_path.partition(":")
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
        self.register(cls())

    @property
    def plugins(self) -> list[Plugin]:
        return list(self._plugins)

    def clear(self) -> None:
        self._plugins.clear()


registry = PluginRegistry()
