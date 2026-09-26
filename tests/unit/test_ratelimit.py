import asyncio
import time
from xscrape.ratelimit import RateLimiter


def test_ratelimiter_waits():
    async def run():
        rl = RateLimiter(rate=10.0, capacity=1)
        await rl.acquire()
        start = time.monotonic()
        await rl.acquire()
        elapsed = time.monotonic() - start
        assert elapsed >= 0.05

    asyncio.run(run())
