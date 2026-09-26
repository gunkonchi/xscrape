"""Example: export search results to CSV."""

import asyncio
from xscrape import XScrapeClient
from xscrape.storage import CsvStorage


async def main() -> None:
    async with XScrapeClient(pool="accounts.json") as client:
        tweets = []
        async for t in client.search("#opensource", limit=500):
            tweets.append(t)

        await CsvStorage("hashtag.csv").save(tweets)
        print(f"Done: {len(tweets)} rows")


if __name__ == "__main__":
    asyncio.run(main())
