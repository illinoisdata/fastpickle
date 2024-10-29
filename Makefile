.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")
USING_POETRY=$(shell grep "tool.poetry" pyproject.toml && echo "yes")

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo " "
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment:"
	@if [ "$(USING_POETRY)" ]; then poetry env info && exit; fi
	@echo "Running using $(ENV_PREFIX)"
	@$(ENV_PREFIX)python -V
	@$(ENV_PREFIX)python -m site

.PHONY: virtualenv
virtualenv:       ## Create a virtual environment.
	@if [ "$(USING_POETRY)" ]; then poetry install && exit; fi
	@echo "creating virtualenv ..."
	@rm -rf .venv
	@python3 -m venv .venv
	@./.venv/bin/pip install -U pip
	@echo
	@echo "!!! Please run 'source .venv/bin/activate' to enable the environment !!!"

.PHONY: install
install:          ## Install the project in dev mode.
	@if [ "$(USING_POETRY)" ]; then poetry install && exit; fi
	$(ENV_PREFIX)pip install -e .[dev]

.PHONY: fmt
fmt:              ## Format code using black & isort.
	$(ENV_PREFIX)isort fastpickle/ tests/
	$(ENV_PREFIX)black -l 127 fastpickle/ tests/

.PHONY: lint
lint:             ## Run pep8, black, mypy linters.
	$(ENV_PREFIX)flake8 --extend-ignore=E203 --max-line-length 127 fastpickle/ tests/
	$(ENV_PREFIX)black -l 127 --check fastpickle/ tests/
	$(ENV_PREFIX)mypy --ignore-missing-imports fastpickle/ tests/

.PHONY: test
test:        ## Run tests and generate coverage report.
	$(ENV_PREFIX)pytest -vv --cov-config .coveragerc --cov=fastpickle -l --tb=short --maxfail=1 tests
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html

.PHONY: clean
clean:            ## Clean unused files.
	@find ./fastpickle -name '*.pyc' -exec rm -f {} \;
	@find ./fastpickle -d -name '__pycache__' -exec rm -rf {} \;
	@find ./fastpickle -name 'Thumbs.db' -exec rm -f {} \;
	@find ./fastpickle -name '*~' -exec rm -f {} \;
	@find ./tests -name '*.pyc' -exec rm -f {} \;
	@find ./tests -d -name '__pycache__' -exec rm -rf {} \;
	@find ./tests -name 'Thumbs.db' -exec rm -f {} \;
	@find ./tests -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
