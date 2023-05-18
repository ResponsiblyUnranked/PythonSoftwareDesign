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
	poetry run pytest tests/ -v

deptry:
	poetry run deptry .

install-dependencies:
	poetry install

lint: isort black ruff mypy
audit: bandit deptry
test: pytest

all: install-dependencies lint audit test