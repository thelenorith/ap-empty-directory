.PHONY: install install-dev test test-verbose lint format coverage clean

install:
	pip install .

install-dev:
	pip install -e ".[dev]"

test:
	pytest

test-verbose:
	pytest -v

lint:
	flake8 ap_empty_directory tests
	black --check ap_empty_directory tests

format:
	black ap_empty_directory tests

coverage:
	pytest --cov=ap_empty_directory --cov-report=term-missing --cov-report=html

clean:
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
