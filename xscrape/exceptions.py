"""Custom exceptions."""


class XScrapeError(Exception):
    """Base exception."""


class AuthError(XScrapeError):
    """Authentication problems (401/403)."""


class RateLimitError(XScrapeError):
    """Rate limit exceeded (429)."""

    def __init__(self, message: str, reset_at: int | None = None):
        super().__init__(message)
        self.reset_at = reset_at


class ParseError(XScrapeError):
    """Failed to parse the response."""


class PoolExhaustedError(XScrapeError):
    """All accounts in the pool are temporarily unavailable."""
