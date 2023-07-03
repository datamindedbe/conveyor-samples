FROM python:3.10.12-slim

# Update python and install dependencies
RUN python -m pip install --upgrade pip setuptools wheel --no-cache-dir
COPY requirements.txt .
RUN python -m pip install --no-cache "soda-core-dbt>=3.0" && \
    python -m pip install --no-cache -r requirements.txt

WORKDIR /app
COPY dbt .

ENV DBT_PROFILES_DIR="/app"
ENV DBT_PROJECT_DIR="/app/quality_coffee"
ENV DBT_USE_COLORS="false"

# Install dependencies
WORKDIR /app/quality_coffee
RUN dbt deps

# Generate dbt manifest
RUN dbt ls

ENTRYPOINT ["dbt"]
