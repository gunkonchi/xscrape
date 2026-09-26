#!/usr/bin/env bash
set -euo pipefail

if [ -f /app/.env ]; then
    # shellcheck disable=SC1091
    set -a; source /app/.env; set +a
fi

exec "$@"
