FROM public.ecr.aws/dataminded/dbt:v1.7.3

WORKDIR /app
COPY . .
WORKDIR /app

# install dependencies
RUN dbt deps

ENV DBT_PROFILES_DIR="/app"
ENV DBT_PROJECT_DIR="/app"

# Using DBT ls makes sure that the DBT cache is populated, this allows DBT to use the cache every time it is started up, this will significantly reduce the startup latency of DBT jobs with many models
RUN dbt ls