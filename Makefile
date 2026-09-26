.PHONY: install dev test lint type fmt docker-build docker-up docker-down clean
 
install:
	pip install -e .

dev:
	pip install -e ".[dev,socks]"
	pre-commit install

test:
	pytest -q

cov:
	pytest --cov=xscrape --cov-report=html

lint:
	ruff check xscrape tests

fmt:
	ruff format xscrape tests

type:
	mypy xscrape

docker-build:
	docker build -f docker/Dockerfile -t xscrape:latest .

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov dist build *.egg-info
