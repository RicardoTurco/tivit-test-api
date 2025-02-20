PROJECT_NAME := tivit-test-api

PYTHONWARNINGS=ignore:Unverified HTTPS request
export PYTHONWARNINGS


setup:
	poetry shell

install:
	poetry install --no-root

run:
	poetry run python main.py

test:
	poetry run pytest -vv -s

test-cov:
	poetry run pytest -vv -s --cov .

test-cov-rep:
	poetry run pytest -vv -s --cov-report html --cov .

clean:
	rm -rf .coverage
	rm -rf htmlcov
