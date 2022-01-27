[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/datamindedbe/lighthouse-datafy-samples)

# lighthouse-datafy-samples
This repository contains a number of sample projects for Datafy 

## Getting started

1. Clone this repostitory
1. Verify you have Datafy CLI installed by executing `datafy doctor`
1. Create an new datafy environment `datafy environment create --name samples`
1. Execute the additional steps listed in the prerequisites folder

## Samples

### MLOps

- titanic: we use the dataset from [Kaggle](https://www.kaggle.com/c/titanic) to build a ml pipeline that will output a model that can be used to predict survival.
- housing: we use the dataset from [Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques) to build a ml pipeline to output a model and another pipeline that will use this model to make predictions on a daily basis.