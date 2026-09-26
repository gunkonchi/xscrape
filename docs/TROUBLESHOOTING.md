# Troubleshooting

## `AuthError: cookie is invalid`

- Ensure `auth_token` and `ct0` are copied completely.
- Verify the session is still active in a browser.
- Check the system clock — large skews cause token rejection.

## `PoolExhaustedError`

- Add more accounts to the pool.
- Reduce `XSCRAPE_CONCURRENCY`.
- Inspect logs for repeated 401/403 responses.

## Frequent `429` responses

- Lower the per-account rate.
- Increase the number of accounts.
- Enable proxies.

## Empty parse results

- Inspect `XSCRAPE_LOG_LEVEL=DEBUG` output.
- Ensure the response body is JSON and not an HTML error page.

## Docker: container exits immediately

- Check `.env` was loaded (`docker compose config`).
- Inspect logs: `docker compose logs -f xscrape`.
