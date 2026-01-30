PYTHON ?= python3

.PHONY: default install install-dev uninstall test test-verbose lint format coverage clean

default: format lint test coverage

install:
	$(PYTHON) -m pip install .

install-dev:
	$(PYTHON) -m pip install -e ".[dev]"

uninstall:
	$(PYTHON) -m pip uninstall -y ap-empty-directory || true

test: install-dev
	$(PYTHON) -m pytest

test-verbose: install-dev
	$(PYTHON) -m pytest -v

lint: install-dev
	$(PYTHON) -m flake8 ap_empty_directory tests --max-line-length=88
	$(PYTHON) -m black --check ap_empty_directory tests

format: install-dev
	$(PYTHON) -m black ap_empty_directory tests

coverage: install-dev
	$(PYTHON) -m pytest --cov=ap_empty_directory --cov-report=term-missing --cov-report=html

clean:
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov || true
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type f -name "*.pyc" -delete || true
