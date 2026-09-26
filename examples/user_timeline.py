"""Example: user timeline."""

import asyncio
from xscrape import XScrapeClient
from xscrape.storage import CsvStorage


async def main() -> None:
    async with XScrapeClient(pool="accounts.json") as client:
        user = await client.user("elonmusk")
        print(f"Profile: {user.name} (@{user.username}), followers: {user.followers}")

        tweets = []
        async for t in client.timeline(user.id, limit=200):
            tweets.append(t)

        await CsvStorage("timeline.csv").save(tweets)
        print(f"Saved {len(tweets)} posts")


if __name__ == "__main__":
    asyncio.run(main())
