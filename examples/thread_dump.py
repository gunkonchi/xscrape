"""Example: reconstruct a full thread."""

import argparse
import asyncio

from xscrape import XScrapeClient
from xscrape.storage import JsonStorage


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("tweet_id")
    parser.add_argument("--out", default="thread.json")
    args = parser.parse_args()

    async with XScrapeClient(pool="accounts.json") as client:
        tweets = await client.thread(args.tweet_id)
        await JsonStorage(args.out).save(tweets)
        print(f"Saved {len(tweets)} posts")


if __name__ == "__main__":
    asyncio.run(main())
