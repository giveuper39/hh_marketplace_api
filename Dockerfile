FROM python:3.10.15-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY poetry.lock pyproject.toml ./
RUN apt update && apt install make
RUN python -m pip install poetry && poetry install --without dev
COPY . .