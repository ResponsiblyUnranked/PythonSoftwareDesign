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
	poetry run pytest -v

deptry:
	poetry run deptry .

install-dependencies:
	poetry install

lint: isort black
audit: ruff mypy bandit deptry
test: pytest

all: install-dependencies lint audit test