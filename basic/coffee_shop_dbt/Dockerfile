FROM public.ecr.aws/dataminded/dbt:v1.4.0

WORKDIR /app
COPY . .
WORKDIR /app/dbt/coffee_shop_dbt

# install dependencies
RUN dbt deps

ENV DBT_PROFILES_DIR="/app/dbt"
ENV DBT_PROJECT_DIR="/app/dbt/coffee_shop_dbt"