# Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for the full guide.

Quick start:

```bash
git clone https://github.com/kloxeld/xscrape.git
cd xscrape
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
pytest -q
```
