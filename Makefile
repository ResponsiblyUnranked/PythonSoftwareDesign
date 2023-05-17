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

deptry:
	poetry run deptry .

lint: isort black ruff mypy
audit: bandit deptry
test: pytest

all: lint audit test