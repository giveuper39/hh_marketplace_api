# Marketplace REST API

This is a simple marketplace REST API written with FastAPI on Python.

## Running the project
#### 1. Install docker, docker compose, make and poetry.
#### 2. Clone this repo.
#### 3. Create .env file with custom db parameters.
#### 4. Run `docker compose up --build` to build the containers and start the server.

### Notes
To filter items with more than one tag simply put `tag_ids` parameter in request multiple times. Example: `curl "http://0.0.0.0:8080/items?tag_ids=1&tag_ids=2" `
