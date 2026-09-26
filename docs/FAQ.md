# FAQ

**Why do requests sometimes return an empty result?**
Most likely a rate limit was hit or the session expired. Check the logs for `429`/`401`.

**How many accounts do I need in the pool?**
At least 3–5 are recommended for stable operation under intensive collection.

**Can I use it without a proxy?**
Yes, but the risk of IP blocking rises under high load.

**Is streaming supported?**
Not yet. See the roadmap.

**How do I export to SQLite?**
```python
from xscrape.storage import SqliteStorage
await SqliteStorage("data.db").save(tweets)
```

**Does it work with SOCKS5 proxies?**
Yes, install the extra: `pip install "xscrape[socks]"`.

**Can I plug my own exporter?**
Yes. Subclass `BaseExporter` and register it with `registry.register(...)`.

**Is there a CLI?**
Yes, run `xscrape --help`.
