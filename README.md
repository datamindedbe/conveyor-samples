[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/datamindedbe/conveyor-samples)

# Conveyor-samples
This repository contains a number of sample projects for Conveyor

## Getting started

1. Clone this repostitory
1. Verify you have the Conveyor CLI installed by executing `conveyor doctor`
1. Authenticate the Conveyor CLI `conveyor auth login`
1. Create an new conveyor environment `conveyor environment create --name samples`
1. Execute the additional steps listed in the prerequisites folder

## Samples

### MLOps

- titanic: we use the dataset from [Kaggle](https://www.kaggle.com/c/titanic) to build a ml pipeline that will output a model that can be used to predict survival.

### Various

- alerting: we use native airflow features to send notifications to Slack.