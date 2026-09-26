"""Utility helpers."""

from __future__ import annotations
import random
import string


def random_ct0(length: int = 32) -> str:
    """Generate a random CSRF token (for tests)."""
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def chunked(seq: list, size: int):
    """Split a list into chunks."""
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def build_query(base: str, **params) -> str:
    """Build a search query with X operators."""
    parts = [base]
    for key, value in params.items():
        if value is None:
            continue
        parts.append(f"{key}:{value}")
    return " ".join(parts)
