"""Token bucket rate limiter."""

from __future__ import annotations
import asyncio
import time


class RateLimiter:
    def __init__(self, rate: float = 1.0, capacity: int = 5):
        """
        :param rate: tokens per second
        :param capacity: maximum bucket size
        """
        self.rate = rate
        self.capacity = capacity
        self._tokens = float(capacity)
        self._last = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1) -> None:
        async with self._lock:
            while True:
                now = time.monotonic()
                elapsed = now - self._last
                self._last = now
                self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)

                if self._tokens >= tokens:
                    self._tokens -= tokens
                    return

                needed = tokens - self._tokens
                await asyncio.sleep(needed / self.rate)
