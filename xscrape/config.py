"""Configuration loader."""

from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    cookies: Optional[str] = None
    pool: Optional[str] = None
    concurrency: int = 4
    timeout: int = 20
    retries: int = 3
    proxy: Optional[str] = None
    user_agent: Optional[str] = None
    log_level: str = "INFO"
    log_format: str = "text"

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            cookies=os.getenv("XSCRAPE_COOKIES"),
            pool=os.getenv("XSCRAPE_POOL"),
            concurrency=int(os.getenv("XSCRAPE_CONCURRENCY", "4")),
            timeout=int(os.getenv("XSCRAPE_TIMEOUT", "20")),
            retries=int(os.getenv("XSCRAPE_RETRIES", "3")),
            proxy=os.getenv("XSCRAPE_PROXY") or None,
            user_agent=os.getenv("XSCRAPE_USER_AGENT"),
            log_level=os.getenv("XSCRAPE_LOG_LEVEL", "INFO"),
            log_format=os.getenv("XSCRAPE_LOG_FORMAT", "text"),
        )
