"""Example: using an account pool."""

import asyncio
from xscrape import XScrapeClient
from xscrape.storage import JsonStorage


async def main() -> None:
    async with XScrapeClient(pool="accounts.json", concurrency=8) as client:
        tweets = []
        async for t in client.search("data engineering", limit=2000):
            tweets.append(t)

        await JsonStorage("data_engineering.json").save(tweets)
        print(f"Collected {len(tweets)} posts using a multi-account pool")


if __name__ == "__main__":
    asyncio.run(main())
