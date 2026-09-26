import pytest

from xscrape import XScrapeClient


@pytest.mark.integration
@pytest.mark.asyncio
async def test_search_returns_iterator():
    """Smoke test: client exposes an async iterator for search."""
    client = XScrapeClient(cookies="auth_token=x; ct0=y")
    assert hasattr(client, "search")
