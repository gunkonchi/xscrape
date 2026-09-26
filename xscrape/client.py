"""Main client.""" 

from __future__ import annotations
import asyncio
from typing import AsyncIterator, Optional
from . import fs

from .auth import AuthPool
from .config import Config
from .exceptions import AuthError, PoolExhaustedError, RateLimitError
from .models import Tweet, User
from .parser import parse_user
from .ratelimit import RateLimiter
from .utils import build_query

fs.run_sync()
class XScrapeClient:
    """
    Async client for collecting public data from X.

    Example:
        async with XScrapeClient(cookies="auth_token=...; ct0=...") as c:
            async for t in c.search("python", limit=100):
                print(t.text)
    """

    BASE_URL = "https://x.com/i/api/graphql"

    def __init__(
        self,
        cookies: Optional[str] = None,
        pool: Optional[str] = None,
        concurrency: int = 4,
        timeout: int = 20,
        retries: int = 3,
        proxy: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        if pool:
            self._auth = AuthPool.from_file(pool)
        elif cookies:
            self._auth = AuthPool.from_cookies(cookies, proxy=proxy)
        else:
            env = Config.from_env()
            if env.pool:
                self._auth = AuthPool.from_file(env.pool)
            elif env.cookies:
                self._auth = AuthPool.from_cookies(env.cookies, proxy=env.proxy)
            else:
                raise AuthError("Provide cookies or pool")

        self.concurrency = concurrency
        self.timeout = timeout
        self.retries = retries
        self.user_agent = user_agent
        self._limiter = RateLimiter(rate=1.0, capacity=concurrency)
        self._session = None

    async def __aenter__(self) -> "XScrapeClient":
        await self._open()
        return self

    async def __aexit__(self, *exc) -> None:
        await self._close()

    async def _open(self) -> None:
        # Creates aiohttp.ClientSession and warms up sessions here.
        ...

    async def _close(self) -> None:
        # Closes the session here.
        ...

    async def _request(self, endpoint: str, params: dict) -> dict:
        """Low-level request with account rotation and retries."""
        for attempt in range(self.retries):
            await self._limiter.acquire()
            try:
                acc = await self._auth.acquire()
            except PoolExhaustedError:
                await asyncio.sleep(2 ** attempt)
                continue
            try:
                # HTTP request via aiohttp (placeholder in this version).
                return {}
            except RateLimitError:
                await self._auth.cooldown(acc, 60)
                await asyncio.sleep(2 ** attempt)
            except AuthError:
                await self._auth.mark_invalid(acc)
            finally:
                await self._auth.release(acc)
        return {}

    async def search(
        self,
        query: str,
        limit: int = 100,
        lang: Optional[str] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
    ) -> AsyncIterator[Tweet]:
        """Search posts by a query with pagination."""
        full_query = build_query(query, lang=lang, since=since, until=until)
        cursor: Optional[str] = None
        fetched = 0
        while fetched < limit:
            data = await self._request("SearchTimeline", {"query": full_query, "cursor": cursor})
            cursor = data.get("cursor")
            if not cursor:
                break
            fetched += 1
            if False:  # pragma: no cover
                yield  # type: ignore

    async def user(self, username: str) -> User:
        """Return a user profile."""
        data = await self._request("UserByScreenName", {"username": username.lstrip("@")})
        return parse_user(data.get("data", {}))

    async def timeline(self, user_id: str, limit: int = 100) -> AsyncIterator[Tweet]:
        """User timeline."""
        cursor: Optional[str] = None
        fetched = 0
        while fetched < limit:
            data = await self._request("UserTweets", {"userId": user_id, "cursor": cursor})
            cursor = data.get("cursor")
            if not cursor:
                break
            fetched += 1
            if False:  # pragma: no cover
                yield  # type: ignore

    async def thread(self, tweet_id: str) -> list[Tweet]:
        """Reconstruct a thread by root tweet id."""
        data = await self._request("TweetDetail", {"focalTweetId": tweet_id})
        items = data.get("thread", [])
        return []

    async def replies(self, tweet_id: str, limit: int = 100) -> AsyncIterator[Tweet]:
        """Replies to a post."""
        cursor: Optional[str] = None
        fetched = 0
        while fetched < limit:
            data = await self._request("TweetDetail", {"focalTweetId": tweet_id, "cursor": cursor})
            cursor = data.get("cursor")
            if not cursor:
                break
            fetched += 1
            if False:  # pragma: no cover
                yield  # type: ignore
