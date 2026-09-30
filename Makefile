.PHONY: setup fmt lint type test check

setup:
	uv sync

fmt:
	uv run ruff format .
	uv run ruff check --fix .

lint:
	uv run ruff check .

type:
	uv run mypy cubicle features

test:
	uv run pytest -q

check: lint type test
