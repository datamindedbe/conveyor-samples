[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/datamindedbe/conveyor-samples)

# Conveyor Samples

This repository contains a number of sample projects for Conveyor

## Getting started

1. Clone this repository
2. Verify you have the Conveyor CLI installed by executing `conveyor doctor`
3. Authenticate the Conveyor CLI `conveyor auth login`
4. Create a new conveyor environment `conveyor environment create --name samples`
5. Execute the additional steps listed in the prerequisites folder

## Samples

### Basic

- pi_spark: use [Apache Spark](https://github.com/apache/spark) to calculate pi.
- coffee_shop_dbt: use [dbt](https://github.com/dbt-labs/dbt-core) and [DuckDB](https://github.com/duckdb/duckdb) 
  for cleaning and transforming the coffee shop input data and writing the results to S3.

### MLOps

- titanic: use the dataset from [Kaggle](https://www.kaggle.com/c/titanic) 
  to build a ML pipeline that will produce a model to predict survival.
- housing: use the dataset from [Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) 
  to build a ML pipeline that will produce a model to predict the housing prices.

### Various

- alerting: use native [Apache Airflow](https://github.com/apache/airflow) features to send notifications to Slack.
