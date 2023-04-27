# Coffee shop

A sample project using [dbt](https://github.com/dbt-labs/dbt-core).

## Prerequisites

- [pyenv](https://github.com/pyenv/pyenv) (recommended)

### Data

Before you can start this sample, you need to copy the raw csv data to an S3 bucket that you created (e.g. `conveyor-samples-*`).
Copy all files to the `conveyor-samples-*` S3 bucket under `coffee-data/raw`. You can use either the AWS Console or the AWS CLI.

```bash
aws s3 cp raw_customers.csv s3://conveyor-samples-*/coffee-data/raw/raw_customers.csv
aws s3 cp raw_items.csv s3://conveyor-samples-*/coffee-data/raw/raw_items.csv
aws s3 cp raw_orders.csv s3://conveyor-samples-*/coffee-data/raw/raw_orders.csv
aws s3 cp raw_products.csv s3://conveyor-samples-*/coffee-data/raw/raw_products.csv
aws s3 cp raw_stores.csv s3://conveyor-samples-*/coffee-data/raw/raw_stores.csv
aws s3 cp raw_supplies.csv s3://conveyor-samples-*/coffee-data/raw/raw_supplies.csv
```

## Code updates

Update the following files to reflect the S3 bucket that you created:

- `dbt/profiles.yml`: change the external_root property
- `dbt/coffee_shop_dbt/models/staging/sources.yml`: update the external location property of the source files

## Project Structure

```bash
root/
 |-- data/
 |-- dags/
 |   |-- project.py
 |-- dbt/
 |   |-- project/
 |   Dockerfile
```

## Concepts

### dbt project structure
Consult the following documentation regarding [best practices for project structure](https://discourse.getdbt.com/t/how-we-structure-our-dbt-projects/355).

## Commands
Start a shell in a container with dbt installed, and your local files mounted:
- `make env` to create a local `.env` file
- `make shell` to start a new shell
- `exit` to terminate the container shell

For some of the most used dbt commands, a makefile has been added to the project that passes the correct flags to dbt. 
These commands assume they are executed in the shell container.
- `make manifest` executes dbt build and copies the `manifest.json` to your dags folder 
- `make run` executes dbt run
- `make test` executes dbt test
- `make debug` executes dbt debug
- `make docs` executes dbt docs

Consult the [dbt documentation](https://docs.getdbt.com/docs/introduction) for additional commands.
