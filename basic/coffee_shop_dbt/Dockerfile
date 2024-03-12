FROM public.ecr.aws/dataminded/dbt:v1.7.3

WORKDIR /app
COPY . .

WORKDIR /app

# install dependencies
RUN dbt deps

ENV DBT_PROFILES_DIR="/app"
ENV DBT_PROJECT_DIR="/app"
ENV DBT_USE_COLORS="false"

# generate dbt manifest
RUN dbt ls
