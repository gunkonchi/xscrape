# Configuration
 
## Sources

1. Environment variables
2. `.env` file (auto-loaded via `python-dotenv`)
3. Constructor arguments of `XScrapeClient(...)`

Priority: arguments > env > `.env`.

## Full option reference

### Authentication

| Option | Env | Description |
|---|---|---|
| `cookies` | `XSCRAPE_COOKIES` | Cookie string with `auth_token` and `ct0` |
| `pool` | `XSCRAPE_POOL` | Path to JSON file with account pool |

### Networking

| Option | Env | Default | Description |
|---|---|---|---|
| `concurrency` | `XSCRAPE_CONCURRENCY` | `4` | Max parallel requests |
| `timeout` | `XSCRAPE_TIMEOUT` | `20` | Per-request timeout, seconds |
| `retries` | `XSCRAPE_RETRIES` | `3` | Retry attempts on failure |
| `proxy` | `XSCRAPE_PROXY` | `None` | Proxy URL |
| `user_agent` | `XSCRAPE_USER_AGENT` | built-in | Custom `User-Agent` header |

### Logging

| Option | Env | Default | Description |
|---|---|---|---|
| `log_level` | `XSCRAPE_LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `log_format` | `XSCRAPE_LOG_FORMAT` | `text` | `text` or `json` |

## Account pool format

`accounts.json`:

```json
[
  {
    "name": "acc1",
    "cookies": "auth_token=...; ct0=...",
    "proxy": "http://user:pass@host:port"
  },
  {
    "name": "acc2",
    "cookies": "auth_token=...; ct0=...",
    "proxy": null
  }
]
```

Attach:
```python
client = XScrapeClient(pool="accounts.json")
```

## Proxies

`http`, `https`, `socks5` are supported. Set them globally (`XSCRAPE_PROXY`) or per account.

## Logging

```python
import logging
logging.getLogger("xscrape").setLevel(logging.DEBUG)
```

JSON logs:
```bash
XSCRAPE_LOG_FORMAT=json xscrape search "python" --limit 10
```
