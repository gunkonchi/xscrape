# Examples

## Search and dump to JSON

```bash
xscrape search "asyncio" --limit 500 --out asyncio.json
```

## Timeline to CSV

```bash
xscrape timeline elonmusk --limit 300 --out timeline.csv
```

## Thread reconstruction

```bash
xscrape thread 1234567890123456789 --out thread.json
```

## Running in Docker

```bash
docker compose run --rm xscrape search "python" --limit 100 --out /data/python.json
```

## Multi-account pool

```bash
XSCRAPE_POOL=accounts.json xscrape hashtag "#opensource" --limit 2000
```

## Long-running monitor

```bash
python examples/hashtag_monitor.py --hashtag "#ai" --interval 60 --out stream.jsonl
```
