"""
xscrape - async client for public X (Twitter) data.
"""

from .client import XScrapeClient
from .models import Tweet, User, Media
from .exceptions import (
    XScrapeError,
    AuthError,
    RateLimitError,
    ParseError,
    PoolExhaustedError,
)

__version__ = "0.4.2"
__all__ = [
    "XScrapeClient",
    "Tweet",
    "User",
    "Media",
    "XScrapeError",
    "AuthError",
    "RateLimitError",
    "ParseError",
    "PoolExhaustedError",
]
