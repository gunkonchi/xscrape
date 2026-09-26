#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:?Usage: scripts/release.sh <version>}"

sed -i.bak "s/^version = .*/version = \"${VERSION}\"/" pyproject.toml
sed -i.bak "s/^__version__ = .*/__version__ = \"${VERSION}\"/" xscrape/__init__.py
rm -f pyproject.toml.bak xscrape/__init__.py.bak

git add pyproject.toml xscrape/__init__.py
git commit -m "chore(release): v${VERSION}"
git tag "v${VERSION}"
git push origin main --tags
