# Rate Limiting

## Strategy

`xscrape` applies a two-level limit:

1. **Global semaphore** — bounds total concurrent in-flight requests.
2. **Per-account token bucket** — smooths the request rate for each session.

## Defaults

| Setting | Default | Notes |
|---|---|---|
| `concurrency` | 4 | Global parallel requests |
| `rate` | 1 req/s | Per account |
| `capacity` | 5 | Bucket size |
| `cooldown_403` | 60 s | Account cooldown on 403 |
| `cooldown_429` | auto | Uses `x-rate-limit-reset` header |

## Tuning

Increase `concurrency` for higher throughput with a larger pool. Decrease the per-account `rate` if you observe frequent `429` responses.

## Backoff

On transient errors the client retries with exponential backoff: `2 ** attempt` seconds, capped at 30 seconds.
