#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev,socks]"
pre-commit install

echo "Bootstrap complete. Run 'source .venv/bin/activate' to start."
