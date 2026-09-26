"""Plugin system."""

from .base import Plugin, PluginContext
from .registry import registry, PluginRegistry

__all__ = ["Plugin", "PluginContext", "registry", "PluginRegistry"]
