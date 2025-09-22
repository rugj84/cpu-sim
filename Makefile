# Use bash for nicer conditional logic
SHELL := /bin/bash

# Default Python version for the project
PY_VERSION ?= 3.13

# Paths
VENV_DIR := .venv
export PYTHONPATH := src


.PHONY: help venv install dev-install sync lock update freeze run test coverage fmt lint fix lint-fix clean reset

help:
	@echo "make venv          - Create local virtual env with uv (Python $(PY_VERSION))"
	@echo "make install       - Create venv (if needed) and install base deps (uv sync)"
	@echo "make dev-install   - Install dev dependencies group (pytest, black, isort, flake8...)"
	@echo "make sync          - Sync deps from pyproject/lock"
	@echo "make lock          - Generate/refresh uv.lock"
	@echo "make update        - Update all deps to latest allowed, refresh lock"
	@echo "make freeze        - Export resolved deps to requirements.lock.txt"
	@echo "make run           - Run the simulator (src/main.py)"
	@echo "make test          - Run tests (pytest)"
	@echo "make coverage      - Run tests with coverage"
	@echo "make fmt           - Format code (black + isort)"
	@echo "make lint          - Lint (flake8)"
	@echo "make fix           - Format + Lint (fail if lint fails)"
	@echo "make clean         - Remove caches/build artifacts"
	@echo "make reset         - Clean + remove .venv"

venv:
	@echo ">>> Ensuring uv virtual environment ($(VENV_DIR)) with Python $(PY_VERSION)"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		uv python install $(PY_VERSION) && \
		uv venv --python $(PY_VERSION) $(VENV_DIR); \
	else \
		echo "$(VENV_DIR) already exists."; \
	fi
	@echo ">>> Activate with: source $(VENV_DIR)/bin/activate (optional; uv run works without activating)."

install: venv
	@echo ">>> Installing base dependencies (uv sync)"
	uv sync

dev-install: venv
	@echo ">>> Installing dev dependencies group (uv sync --group dev)"
	uv sync --group dev

sync:
	@echo ">>> Syncing dependencies"
	uv sync

lock:
	@echo ">>> Generating uv.lock"
	uv lock

update:
	@echo ">>> Updating dependencies to latest compatible versions and refreshing lock"
	uv lock --upgrade

freeze:
	@echo ">>> Writing fully resolved dependency set to requirements.lock.txt"
	uv pip freeze > requirements.lock.txt
	@echo "requirements.lock.txt updated."

test:
	@echo ">>> Ensuring dev deps"
	uv sync --group dev
	@echo ">>> Running tests"
	uv run pytest

coverage:
	@echo ">>> Running tests with coverage"
	uv run pytest -v --cov=src --cov-report=term-missing

run:
	@echo ">>> Running CPU Simulator"
	uv run python -m cpu_sim.main


fmt:
	@echo ">>> Formatting with black and isort"
	uv run black src tests
	uv run isort src tests

lint:
	@echo ">>> Linting with flake8"
	uv run flake8 src tests

fix: fmt lint

clean:
	@echo ">>> Cleaning build and cache artifacts"
	@rm -rf .pytest_cache
	@rm -rf build dist *.egg-info
	@find . -name "__pycache__" -type d -prune -exec rm -rf {} +

reset: clean
	@echo ">>> Removing virtual environment"
	@rm -rf $(VENV_DIR)

