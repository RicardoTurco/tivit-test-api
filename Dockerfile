FROM python:3.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

ENV POETRY_VERSION=1.8.2

RUN apt-get update && apt-get install -y wkhtmltopdf

WORKDIR /app
COPY . /app/

SHELL ["/bin/bash", "-c"]

RUN pip install --upgrade pip && \
    pip install poetry==$POETRY_VERSION && \
    poetry install --no-root

EXPOSE 8080