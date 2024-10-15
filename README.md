# Marketplace REST API

This is a simple marketplace REST API written with FastAPI on Python.

## Running the project
#### 1. Install Docker and docker-compose
#### 2. Clone this repo.
#### 3. Create .env file with custom db parameters (like in the example).
#### 4. Run `docker compose up --build` to build the containers and start the server.

### Notes
To filter items with more than one tag simply put `tag_ids` parameter in request multiple times. Example: `curl "http://0.0.0.0:8080/items?tag_ids=1&tag_ids=2"`.

### Running tests locally
To run tests locally, change database to sqlite in `app/db.py` (for simplicity). To setup everything locally run `poetry install`. And to run tests simply run `make test` and `make lint` for linter (ruff).
