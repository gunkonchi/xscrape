# syntax=docker/dockerfile:1.6 

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates curl tini \
    && rm -rf /var/lib/apt/lists/*

# --- Builder stage ---
FROM base AS builder

COPY pyproject.toml requirements.txt README.md ./
COPY xscrape ./xscrape

RUN pip install --upgrade pip build \
    && pip install --prefix=/install -r requirements.txt \
    && pip install --prefix=/install .

# --- Runtime stage ---
FROM base AS runtime

COPY --from=builder /install /usr/local
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
COPY examples ./examples

RUN chmod +x /usr/local/bin/entrypoint.sh \
    && useradd --create-home --shell /bin/bash appuser \
    && mkdir -p /data && chown -R appuser:appuser /data /app

USER appuser

VOLUME ["/data"]
WORKDIR /app

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/bin/entrypoint.sh"]
CMD ["xscrape", "--help"]
