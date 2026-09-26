"""Example: export results to SQLite."""
 
import asyncio
from xscrape import XScrapeClient
from xscrape.storage import SqliteStorage


async def main() -> None:
    async with XScrapeClient(pool="accounts.json") as client:
        tweets = []
        async for t in client.search("machine learning", limit=1000):
            tweets.append(t)

        await SqliteStorage("ml.db").save(tweets)
        print(f"Stored {len(tweets)} posts in ml.db")


if __name__ == "__main__":
    asyncio.run(main())
