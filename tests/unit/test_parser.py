from xscrape.parser import parse_tweet


def test_parse_minimal_tweet():
    raw = {
        "rest_id": "1",
        "legacy": {
            "full_text": "hello world",
            "id_str": "1",
            "created_at": "Mon Jan 01 00:00:00 +0000 2024",
        },
    }
    tweet = parse_tweet(raw)
    assert tweet.id == "1"
    assert tweet.text == "hello world"
