.PHONY: venv install browsers fmt lint test ci clean precommit

PYTHON ?= python3.13
VENV=.venv

venv:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate; pip install --upgrade pip

install: venv
	. $(VENV)/bin/activate; pip install -e .[dev]
	. $(VENV)/bin/activate; python -m playwright install chromium

browsers:
	. $(VENV)/bin/activate; python -m playwright install --with-deps chromium

fmt:
	. $(VENV)/bin/activate; black .

lint:
	. $(VENV)/bin/activate; flake8 src tests
	. $(VENV)/bin/activate; mypy src

TEST_ARGS ?=

test:
	. $(VENV)/bin/activate; pytest -p no:rerunfailures $(TEST_ARGS)

ci:
	pytest -n auto --maxfail=1 --cov=src --cov-report xml:artifacts/coverage.xml --reruns 1 --reruns-delay 1

precommit:
	. $(VENV)/bin/activate; pre-commit install

clean:
	rm -rf .pytest_cache artifacts allure-report report.html site build
