lint:
	poetry run ruff check app tests

test:
	poetry run pytest --cov

run:
	poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080
