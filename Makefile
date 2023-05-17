.DEFAULT_GOAL := all

mypy:
	poetry run mypy .

ruff:
	poetry run ruff check .

black:
	poetry run black .

isort:
	poetry run isort .

bandit:
	poetry run bandit -c pyproject.toml -r .

pytest:
	poetry run pytest tests/

lint: isort black ruff mypy
audit: bandit
test: pytest

all: lint audit test