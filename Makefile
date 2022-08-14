.PHONY: test
test:
	python -m pytest

.PHONY: lint
lint:
	flake8 src
	isort --check --diff src
	black --check src

.PHONY: format
format:
	isort src
	black src
