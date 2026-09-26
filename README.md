# xscrape

> Asynchronous Python client for collecting public data from X (Twitter).

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Version](https://img.shields.io/badge/version-0.4.2-orange)]()
[![Docker](https://img.shields.io/badge/docker-ready-blue)]()

**xscrape** is a lightweight library for asynchronously collecting public data from X (Twitter): posts, profiles, threads, replies, and media. It supports account rotation, a built-in rate limiter, and export to JSON / CSV / SQLite.

---

## Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [How It Works](#-how-it-works)
- [Configuration](#-configuration)
- [CLI](#-cli)
- [Examples](#-examples)
- [Docker](#-docker)
- [Testing](#-testing)
- [Project Layout](#-project-layout)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## Features

- 🔍 **Post search** — by keywords, hashtags, and operators (`from:`, `since:`, `until:`)
- 👤 **User profiles** — metadata, followers, activity counters
- 🧵 **Threads and replies** — reconstruction of conversation chains
- 🖼 **Media** — extraction of image and video links
- 🔄 **Account rotation** — session pool with automatic failover
- ⏱ **Rate limiting** — adaptive control of request frequency
- 💾 **Storage backends** — JSON, CSV, SQLite out of the box
- 🧩 **Plugins** — custom handlers and exporters
- 🖥 **CLI** — ready-to-use command line interface
- 🐳 **Docker-ready** — single command deployment
- 📊 **Structured logging** — JSON logs with request tracing

---

## 📦 Installation

### From source
```bash
git clone https://github.com/kloxeld/xscrape.git
cd xscrape
pip install -e .
```

### Requirements
- Python 3.10+
- `aiohttp`, `pydantic`, `tenacity`, `orjson`

### Optional
```bash
pip install "xscrape[socks]"    # SOCKS proxy support
pip install "xscrape[dev]"      # development tools
pip install "xscrape[docs]"     # documentation builders
```

---

##  Quick Start

```bash

# Search posts
xscrape search "python asyncio" --limit 50 --out tweets.json

# User profile
xscrape user elonmusk

# User timeline
xscrape timeline elonmusk --limit 200 --out timeline.csv

# Reconstruct a thread
xscrape thread 1234567890123456789 --out thread.json

# Collect by hashtag into SQLite
xscrape hashtag "#opensource" --limit 1000 --db hashtag.db

# Multi-account pool
XSCRAPE_POOL=accounts.json xscrape search "data engineering" --limit 2000

```
Run `xscrape --help` for the full command reference.

##  How It Works

`xscrape` talks to public GraphQL endpoints of X using session cookies. The pipeline looks like this:

```
┌────────────┐   ┌──────────────┐   ┌────────────┐   ┌────────────┐
│  Client    │──▶│  AuthPool    │──▶│  Fetcher   │──▶│  Parser    │
└────────────┘   └──────────────┘   └────────────┘   └────────────┘
                                            │                │
                                            ▼                ▼
                                     ┌────────────┐   ┌────────────┐
                                     │ RateLimiter│   │  Storage   │
                                     └────────────┘   └────────────┘
```

1. **Client** — public interface (`search`, `user`, `thread`, `replies`).
2. **AuthPool** — session pool; picks a free account, handles 429/401.
3. **Fetcher** — low-level HTTP requests with retries and exponential backoff.
4. **Parser** — normalizes raw responses into typed models (`Tweet`, `User`).
5. **RateLimiter** — per-account token bucket plus a global cap.
6. **Storage** — serialization of results into the chosen format.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for details.

---

##  Configuration

All options are read from environment variables (see `.env.example`):

| Variable | Description | Default |
|---|---|---|
| `XSCRAPE_COOKIES` | Cookie string (`auth_token`, `ct0`) | — |
| `XSCRAPE_POOL` | Path to JSON with account pool | `None` |
| `XSCRAPE_CONCURRENCY` | Max parallel requests | `4` |
| `XSCRAPE_TIMEOUT` | Request timeout (seconds) | `20` |
| `XSCRAPE_RETRIES` | Number of retries on error | `3` |
| `XSCRAPE_USER_AGENT` | Custom User-Agent | built-in |
| `XSCRAPE_PROXY` | Proxy (`http://user:pass@host:port`) | `None` |
| `XSCRAPE_LOG_LEVEL` | Logging level | `INFO` |
| `XSCRAPE_LOG_FORMAT` | `text` or `json` | `text` |

Full reference: [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

---


## Examples

The [`examples/`](examples/) directory contains ready-to-run scripts:

- `search_tweets.py` — search with pagination and filters
- `user_timeline.py` — collect a user's timeline
- `export_to_csv.py` — dump results to CSV
- `export_to_sqlite.py` — persist results into SQLite
- `thread_dump.py` — reconstruct a full thread
- `hashtag_monitor.py` — long-running hashtag watcher
- `multi_account_pool.py` — usage of an account pool

Run:
```bash
python examples/search_tweets.py --query "openai" --limit 200
```

---

## 🐳 Docker

### Build
```bash
docker build -f docker/Dockerfile -t xscrape:latest .
```

### Run with docker-compose
```bash
cp .env.example .env
docker compose up --build
```

### Development stack
```bash
docker compose -f docker-compose.dev.yml up --build
```

See [docs/EXAMPLES.md](docs/EXAMPLES.md) for advanced Docker workflows.

---

## Testing

```bash
pytest -q                    # run everything
pytest tests/unit            # unit tests only
pytest tests/integration     # integration tests only
```

Coverage:
```bash
pytest --cov=xscrape --cov-report=html
```

---

## Project Layout

```
xscrape/
├── xscrape/          # library source
│   ├── client.py     # public client
│   ├── auth.py       # session pool
│   ├── parser.py     # response parsing
│   ├── ratelimit.py  # rate limiter
│   ├── storage.py    # storage backends
│   ├── plugins/      # plugin system
│   └── exporters/    # pluggable exporters
├── tests/            # unit + integration tests
├── examples/         # ready-to-run scripts
├── docs/             # documentation
├── docker/           # Dockerfiles
├── scripts/          # helper shell scripts
└── .github/          # CI workflows, templates
```

---

## Roadmap

- [x] Search and profiles
- [x] Account pool and rate limiter
- [x] JSON / CSV / SQLite export
- [x] CLI
- [x] Docker support
- [ ] Plugin exporter system
- [ ] Media download support
- [ ] Webhook notifications
- [ ] Web monitoring dashboard
- [ ] Prometheus metrics
- [ ] GraphQL query cache

Full roadmap: [docs/ROADMAP.md](docs/ROADMAP.md).

---

## Contributing

We welcome contributions. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before opening a PR.

---

## ⚠️ Disclaimer

This project is intended **for educational purposes and work with public data only**. Use it in accordance with the laws of your jurisdiction and the platform's rules. The authors are not responsible for any consequences of use.

---

## License

MIT — see [LICENSE](LICENSE).
