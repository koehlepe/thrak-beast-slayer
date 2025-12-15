.PHONY: help install install-dev format lint type-check test clean run

help:
	@echo "Thrak Beast Slayer - Development Tasks"
	@echo "========================================"
	@echo "make install       - Install production dependencies"
	@echo "make install-dev   - Install development dependencies"
	@echo "make format        - Format code with Black"
	@echo "make lint          - Run linting checks (Flake8 + Pylint)"
	@echo "make type-check    - Run type checking with mypy"
	@echo "make test          - Run test suite"
	@echo "make clean         - Remove build artifacts and cache"
	@echo "make run           - Run the game"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

format:
	black . --line-length=100

lint:
	flake8 . --count --show-source --statistics
	pylint --disable=all --enable=E,F main.py config.py types.py

type-check:
	mypy . --ignore-missing-imports --no-error-summary

test:
	pytest -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	rm -rf dist/ build/ *.egg-info/ 2>/dev/null || true

run:
	python main.py
