FROM python:3.7-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

WORKDIR /app/dbt/openaqdbt

#CMD dbt run --target ${TARGET} --profiles-dir .
