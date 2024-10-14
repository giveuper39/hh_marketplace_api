lint:
	poetry run ruff check app tests
	poetry run mypy app

test:
	poetry run pytest --cov

run:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080

build:
	rm -rf dist/* && poetry build