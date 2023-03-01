FROM public.ecr.aws/dataminded/dbt:v1.4.0

WORKDIR /app
COPY . .

RUN mv upstream-patch.sql /usr/local/lib/python3.10/site-packages/dbt/include/duckdb/macros/utils/upstream.sql

WORKDIR /app/dbt/coffee_shop_dbt

# install dependencies
RUN dbt deps

ENV DBT_PROFILES_DIR="/app/dbt"
ENV DBT_PROJECT_DIR="/app/dbt/coffee_shop_dbt"
ENV DBT_USE_COLORS="false"
RUN dbt ls