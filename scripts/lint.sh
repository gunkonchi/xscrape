#!/usr/bin/env bash 
set -euo pipefail

ruff check xscrape tests
ruff format --check xscrape tests
mypy xscrape
