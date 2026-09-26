# Contributing

Thanks for considering contributing to `xscrape`!

## Development setup

```bash
git clone https://github.com/yourname/xscrape.git
cd xscrape
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Running tests

```bash
pytest -q
ruff check xscrape tests
mypy xscrape
```

## Commit style

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(client): add support for cursor pagination
fix(parser): handle missing user_results
docs(readme): clarify proxy configuration
```

## Pull requests

1. Fork the repo and create a feature branch.
2. Add tests for any new behavior.
3. Ensure `ruff`, `mypy`, and `pytest` pass locally.
4. Open a PR using the template.
