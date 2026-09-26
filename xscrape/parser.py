"""Parsing of raw responses into models."""

from __future__ import annotations
from datetime import datetime
from typing import Any

from .exceptions import ParseError
from .models import Media, Tweet, User


def _dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%a %b %d %H:%M:%S %z %Y")
    except ValueError:
        return None


def parse_user(raw: dict[str, Any]) -> User:
    try:
        legacy = raw.get("legacy", raw)
        return User(
            id=str(raw.get("rest_id") or legacy.get("id_str")),
            username=legacy.get("screen_name", ""),
            name=legacy.get("name"),
            bio=legacy.get("description"),
            followers=legacy.get("followers_count", 0),
            following=legacy.get("friends_count", 0),
            tweets_count=legacy.get("statuses_count", 0),
            verified=bool(raw.get("is_blue_verified") or legacy.get("verified")),
            created_at=_dt(legacy.get("created_at")),
            avatar_url=legacy.get("profile_image_url_https"),
        )
    except (KeyError, TypeError) as e:
        raise ParseError(f"Failed to parse User: {e}") from e


def parse_media(raw: dict[str, Any]) -> list[Media]:
    entities = raw.get("extended_entities") or raw.get("entities") or {}
    items = entities.get("media", []) or []
    return [
        Media(
            type=m.get("type", "photo"),
            url=m.get("media_url_https", ""),
            preview_url=m.get("media_url_https"),
        )
        for m in items
    ]


def parse_tweet(raw: dict[str, Any]) -> Tweet:
    try:
        legacy = raw.get("legacy", raw)
        user_raw = (
            raw.get("core", {}).get("user_results", {}).get("result")
            or raw.get("user", {})
        )
        author = parse_user(user_raw) if user_raw else User(id="0", username="unknown")

        hashtags = [h.get("text", "") for h in legacy.get("entities", {}).get("hashtags", [])]
        mentions = [m.get("screen_name", "") for m in legacy.get("entities", {}).get("user_mentions", [])]
        urls = [u.get("expanded_url", "") for u in legacy.get("entities", {}).get("urls", [])]

        return Tweet(
            id=str(raw.get("rest_id") or legacy.get("id_str")),
            text=legacy.get("full_text") or legacy.get("text", ""),
            author=author,
            created_at=_dt(legacy.get("created_at")),
            lang=legacy.get("lang"),
            likes=legacy.get("favorite_count", 0),
            retweets=legacy.get("retweet_count", 0),
            replies=legacy.get("reply_count", 0),
            quotes=legacy.get("quote_count", 0),
            views=int((raw.get("views") or {}).get("count", 0) or 0) or None,
            media=parse_media(legacy),
            is_reply=bool(legacy.get("in_reply_to_status_id_str")),
            reply_to_id=legacy.get("in_reply_to_status_id_str"),
            conversation_id=legacy.get("conversation_id_str"),
            hashtags=hashtags,
            mentions=mentions,
            urls=urls,
        )
    except (KeyError, TypeError) as e:
        raise ParseError(f"Failed to parse Tweet: {e}") from e
