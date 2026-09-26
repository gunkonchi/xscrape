# Architecture

## Overview

`xscrape` is built around an asynchronous pipeline split into independent layers. Each layer can be replaced or extended without touching the others.

## Layers

### 1. Client (`xscrape/client.py`)
User-facing facade. Methods:
- `search(query, limit, lang, ...) -> AsyncIterator[Tweet]`
- `user(username) -> User`
- `timeline(user_id, limit) -> AsyncIterator[Tweet]`
- `thread(tweet_id) -> list[Tweet]`
- `replies(tweet_id, limit) -> AsyncIterator[Tweet]`

### 2. AuthPool (`xscrape/auth.py`)
Manages the session pool. Capabilities:
- loads cookies from `.env` or a JSON file,
- marks an account as busy during a request,
- temporarily excludes an account on 429/403,
- periodically validates session freshness.

### 3. Fetcher (inside `client.py`)
Wrapper over `aiohttp.ClientSession` with:
- retries via `tenacity`,
- exponential backoff,
- proxy support,
- custom headers.

### 4. Parser (`xscrape/parser.py`)
Converts JSON responses into `Tweet`, `User`, `Media` models. Tolerant to missing fields (uses `.get()` and defaults).

### 5. RateLimiter (`xscrape/ratelimit.py`)
Token bucket per account plus a global semaphore. Configured via `XSCRAPE_CONCURRENCY`.

### 6. Storage (`xscrape/storage.py`)
Abstract `BaseStorage` with implementations:
- `JsonStorage`
- `CsvStorage`
- `SqliteStorage`

### 7. Plugins (`xscrape/plugins/`)
Registry of extension points. Plugins can hook into `on_request`, `on_response`, `on_parse`, and `on_save`.

### 8. Exporters (`xscrape/exporters/`)
Pluggable exporters implementing `BaseExporter`. Register custom ones via `registry.register(...)`.

## Data flow

```
search() ──▶ AuthPool.acquire() ──▶ Fetcher.get() ──▶ Parser.parse()
   ▲                                                        │
   └──────────── RateLimiter.wait() ◀──── Storage.save() ◀──┘
```

## Error handling

| Code | Action |
|---|---|
| 401 | Mark account invalid, take the next one |
| 403 | Backoff 60s, rotate account |
| 429 | Read `x-rate-limit-reset`, wait |
| 5xx | Retry with exponential backoff |

## Concurrency model

- One `aiohttp.ClientSession` shared across requests.
- A global `asyncio.Semaphore` bounds concurrent requests.
- Each account has its own token bucket in the rate limiter.
- Fetchers are cancellation-safe and shut down cleanly on `__aexit__`.

## Extending

To add a new storage backend, subclass `BaseStorage` and implement `save`. To add a new exporter, subclass `BaseExporter` and register it. To hook into the pipeline, implement a plugin using `xscrape.plugins.base.Plugin`.
