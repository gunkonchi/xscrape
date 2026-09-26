"""Command line interface for xscrape."""

from __future__ import annotations
import asyncio
from pathlib import Path

import click
from rich.console import Console

from .client import XScrapeClient
from .storage import CsvStorage, JsonStorage, SqliteStorage

console = Console()


def _storage_from_path(path: str):
    suffix = Path(path).suffix.lower()
    if suffix == ".json":
        return JsonStorage(path)
    if suffix == ".csv":
        return CsvStorage(path)
    if suffix in {".db", ".sqlite", ".sqlite3"}:
        return SqliteStorage(path)
    raise click.BadParameter(f"Unsupported output format: {suffix}")


@click.group()
@click.version_option()
def main() -> None:
    """xscrape - collect public data from X (Twitter)."""


@main.command()
@click.argument("query")
@click.option("--limit", type=int, default=100, show_default=True)
@click.option("--lang", default=None)
@click.option("--out", default="out.json", show_default=True)
def search(query: str, limit: int, lang: str | None, out: str) -> None:
    """Search posts by a query."""
    async def run() -> None:
        async with XScrapeClient() as client:
            tweets = []
            async for tweet in client.search(query, limit=limit, lang=lang):
                tweets.append(tweet)
                console.print(f"[cyan]{tweet.author.username}[/cyan]: {tweet.text[:80]}")
            await _storage_from_path(out).save(tweets)
            console.print(f"[green]Saved {len(tweets)} posts to {out}[/green]")

    asyncio.run(run())


@main.command()
@click.argument("username")
@click.option("--limit", type=int, default=100, show_default=True)
@click.option("--out", default="timeline.json", show_default=True)
def timeline(username: str, limit: int, out: str) -> None:
    """Collect a user's timeline."""
    async def run() -> None:
        async with XScrapeClient() as client:
            user = await client.user(username)
            console.print(f"[bold]{user.name}[/bold] (@{user.username})")
            tweets = []
            async for tweet in client.timeline(user.id, limit=limit):
                tweets.append(tweet)
            await _storage_from_path(out).save(tweets)
            console.print(f"[green]Saved {len(tweets)} posts to {out}[/green]")

    asyncio.run(run())


@main.command()
@click.argument("tweet_id")
@click.option("--out", default="thread.json", show_default=True)
def thread(tweet_id: str, out: str) -> None:
    """Reconstruct a thread by root tweet id."""
    async def run() -> None:
        async with XScrapeClient() as client:
            tweets = await client.thread(tweet_id)
            await _storage_from_path(out).save(tweets)
            console.print(f"[green]Saved {len(tweets)} posts to {out}[/green]")

    asyncio.run(run())


@main.command()
@click.argument("hashtag")
@click.option("--limit", type=int, default=500, show_default=True)
@click.option("--db", default="hashtag.db", show_default=True)
def hashtag(hashtag: str, limit: int, db: str) -> None:
    """Collect posts by a hashtag into a SQLite database."""
    async def run() -> None:
        async with XScrapeClient() as client:
            tweets = []
            async for tweet in client.search(hashtag, limit=limit):
                tweets.append(tweet)
            await SqliteStorage(db).save(tweets)
            console.print(f"[green]Saved {len(tweets)} posts to {db}[/green]")

    asyncio.run(run())


if __name__ == "__main__":
    main()
