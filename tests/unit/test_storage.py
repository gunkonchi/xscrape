import json
import pytest

from xscrape.models import Tweet, User
from xscrape.storage import JsonStorage


@pytest.mark.asyncio
async def test_json_storage(tmp_path):
    tweet = Tweet(
        id="1",
        text="hello",
        author=User(id="u1", username="alice"),
    )
    path = tmp_path / "out.json"
    await JsonStorage(path).save([tweet])
    data = json.loads(path.read_text())
    assert data[0]["id"] == "1"
