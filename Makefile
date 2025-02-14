PROJECT_NAME := tivit-test-api

setup:
	poetry shell

install:
	poetry install --no-root

run:
	poetry run python main.py

test:
	poetry run pytest -v

test-cov:
	poetry run pytest -v --cov .

test-cov-rep:
	poetry run pytest -v --cov-report html --cov .

clean:
	rm -rf .coverage
	rm -rf htmlcov
