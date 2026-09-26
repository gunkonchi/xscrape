"""Typed data models."""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Media(BaseModel):
    type: str                     # "photo" | "video" | "gif"
    url: str
    preview_url: Optional[str] = None


class User(BaseModel):
    id: str
    username: str
    name: Optional[str] = None
    bio: Optional[str] = None
    followers: int = 0
    following: int = 0
    tweets_count: int = 0
    verified: bool = False
    created_at: Optional[datetime] = None
    avatar_url: Optional[str] = None


class Tweet(BaseModel):
    id: str
    text: str
    author: User
    created_at: Optional[datetime] = None
    lang: Optional[str] = None
    likes: int = 0
    retweets: int = 0
    replies: int = 0
    quotes: int = 0
    views: Optional[int] = None
    media: list[Media] = Field(default_factory=list)
    is_reply: bool = False
    is_retweet: bool = False
    reply_to_id: Optional[str] = None
    conversation_id: Optional[str] = None
    hashtags: list[str] = Field(default_factory=list)
    mentions: list[str] = Field(default_factory=list)
    urls: list[str] = Field(default_factory=list)

    def to_dict(self) -> dict:
        return self.model_dump(mode="json")
