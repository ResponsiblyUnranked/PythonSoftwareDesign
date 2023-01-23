.DEFAULT_GOAL := all

mypy:
	poetry run mypy .

flake8:
	poetry run flake8 . --exclude .git,.mypy_cache,.pytest_cache,.venv

black:
	poetry run black .

isort:
	poetry run isort .

bandit:
	poetry run bandit -c pyproject.toml -r .

pytest:
	poetry run pytest tests/

lint: isort black flake8 mypy
audit: bandit
test: pytest

all: lint audit test