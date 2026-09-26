"""Example: long-running hashtag monitor."""

import argparse
import asyncio
import json
import time

from xscrape import XScrapeClient


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hashtag", required=True)
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--out", default="stream.jsonl")
    args = parser.parse_args()

    seen: set[str] = set()

    async with XScrapeClient(pool="accounts.json") as client:
        while True:
            async for tweet in client.search(args.hashtag, limit=100):
                if tweet.id in seen:
                    continue
                seen.add(tweet.id)
                with open(args.out, "a", encoding="utf-8") as f:
                    f.write(json.dumps(tweet.to_dict(), ensure_ascii=False) + "\n")
            await asyncio.sleep(args.interval)


if __name__ == "__main__":
    asyncio.run(main())
