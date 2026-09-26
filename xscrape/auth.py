"""Session account pool."""

from __future__ import annotations
import asyncio
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .exceptions import AuthError, PoolExhaustedError


@dataclass
class Account:
    name: str
    cookies: str
    proxy: Optional[str] = None
    invalid: bool = False
    cooldown_until: float = 0.0
    busy: bool = field(default=False)

    def as_cookie_dict(self) -> dict[str, str]:
        result: dict[str, str] = {}
        for pair in self.cookies.split(";"):
            if "=" in pair:
                k, v = pair.strip().split("=", 1)
                result[k] = v
        return result


class AuthPool:
    """Manages a set of accounts and their state."""

    def __init__(self, accounts: list[Account]):
        if not accounts:
            raise AuthError("AuthPool is empty: add at least one account")
        self._accounts = accounts
        self._lock = asyncio.Lock()

    @classmethod
    def from_file(cls, path: str | Path) -> "AuthPool":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        accounts = [
            Account(
                name=item["name"],
                cookies=item["cookies"],
                proxy=item.get("proxy"),
            )
            for item in data
        ]
        return cls(accounts)

    @classmethod
    def from_cookies(cls, cookies: str, proxy: Optional[str] = None) -> "AuthPool":
        return cls([Account(name="default", cookies=cookies, proxy=proxy)])

    async def acquire(self) -> Account:
        async with self._lock:
            now = asyncio.get_event_loop().time()
            for acc in self._accounts:
                if acc.invalid or acc.busy or acc.cooldown_until > now:
                    continue
                acc.busy = True
                return acc
            raise PoolExhaustedError("No accounts available")

    async def release(self, acc: Account) -> None:
        async with self._lock:
            acc.busy = False

    async def mark_invalid(self, acc: Account) -> None:
        async with self._lock:
            acc.invalid = True

    async def cooldown(self, acc: Account, seconds: float) -> None:
        async with self._lock:
            acc.cooldown_until = asyncio.get_event_loop().time() + seconds

    def __len__(self) -> int:
        return len(self._accounts)
