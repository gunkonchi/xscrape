import pytest
from xscrape import XScrapeClient


@pytest.mark.asyncio
async def test_client_requires_auth(monkeypatch):
    monkeypatch.delenv("XSCRAPE_COOKIES", raising=False)
    monkeypatch.delenv("XSCRAPE_POOL", raising=False)
    with pytest.raises(Exception):
        XScrapeClient()


@pytest.mark.asyncio
async def test_client_accepts_cookies():
    client = XScrapeClient(cookies="auth_token=x; ct0=y")
    assert client is not None
