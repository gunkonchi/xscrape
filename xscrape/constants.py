"""Project-wide constants."""

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

BASE_URL = "https://x.com/i/api/graphql"

ENDPOINTS = {
    "search": "SearchTimeline",
    "user": "UserByScreenName",
    "timeline": "UserTweets",
    "tweet_detail": "TweetDetail",
    "followers": "Followers",
    "following": "Following",
    "likes": "Likes",
}

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

RETRY_BACKOFF_BASE = 2
RETRY_BACKOFF_MAX = 30
COOLDOWN_ON_403 = 60
