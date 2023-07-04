FROM python:3.10.12-slim

# Update python and install dependencies
RUN python -m pip install --upgrade pip setuptools wheel --no-cache-dir
COPY requirements.txt .
RUN python -m pip install --no-cache -r requirements.txt

WORKDIR /app
COPY dbt .

# Set environment variables
ENV DBT_USE_COLORS="false"

# Install dependencies
RUN dbt deps

# Generate dbt manifest
RUN dbt ls

ENTRYPOINT ["dbt"]
