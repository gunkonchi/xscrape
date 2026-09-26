"""Example: search posts by a query."""

import argparse
import asyncio

from xscrape import XScrapeClient
from xscrape.storage import JsonStorage


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--out", default="out.json")
    args = parser.parse_args()

    async with XScrapeClient(pool="accounts.json") as client:
        results = []
        async for tweet in client.search(args.query, limit=args.limit):
            results.append(tweet)
            print(f"{tweet.author.username}: {tweet.text[:80]}")

        await JsonStorage(args.out).save(results)
        print(f"Saved {len(results)} posts to {args.out}")


if __name__ == "__main__":
    asyncio.run(main())
