# Titanic

In this example we use the dataset from [Kaggle](https://www.kaggle.com/c/titanic) to build a ml model that can be used to predict survival. 
We move from experiment to industrialization and cover the steps of data analysis, data preparation, model training and model evaluation. 

## Prerequisites

### Data

Before you can start this sample, you need to copy the data from Kaggle to the s3 bucket created as a prerequisite.

1. Open https://www.kaggle.com/ and login or register (it's free)
1. Navigate to https://www.kaggle.com/c/titanic and download the `test.csv` and `train.csv` in the data tab
1. Copy both files to the `datafy-samples-*` s3 bucket under `titanic/raw`. You can use either the AWS Console or the AWS CLI.

```bash
aws s3 cp test.csv s3://datafy-samples-*/titanic/raw/test.csv
aws s3 cp test.csv s3://datafy-samples-*/titanic/raw/train.csv
```


## Quickstart

1. Initialize this folder as a project: `datafy project create --name samples_titanic`
1. Build the project: `datafy build`
1. Deploy the project to the samples environment: `datafy deploy --env samples --wait`
1. Run the created workflow:
    1. Navigate to `https://app.datafy.cloud/environments` and select the `samples` environment
    1. Press the play button next to the `samples_titanic` dag in airflow to manually trigger the pipeline


## Walkthrough

Navigate to this folder and initialize it as a datafy project `datafy project create --name samples_titanic`. Next we recommend opening the folder
in VSCode 

### Experiment

#### Data analysis

First we explore and analyse the data. To do this we use the notebook feature of datafy. Execute `datafy notebook create --env samples`.
This will package the code, publish it and start a new Jupyter notebook that will open in your browser window. This might take a while the first time. In Jupyter, open `notebooks/exploration.ipynb`. Execute the cells in the notebook and see how we used this to gain a better understanding of the data.

We don't take credit for this effort. All thanks goes to https://medium.com/analytics-vidhya/exploratory-data-analysis-of-titanic-survival-problem-e3af0fb1f276.

#### Building a first model

The next step is to find a first suitable model. In Jupyter, open `notebooks/model.ipynb`. Execute the cells in the notebook and see how we use our understanding of the data done in the previous step, to build features, evaluate their importance and try a number of models. 

Once we find a model, that is good enough, we can start the automation process.

### Industrialization

As described by Google as [MLOps](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) we will automate a pipeline that consists of: 

1. data validation
1. data preparation
1. model training
1. model evalution

For simplicity sake, we will not cover the step of model validation in this sample. 

#### Data validation

In this step we will use the [pandera](https://pandera.readthedocs.io/en/stable/) library to validate our data. To iterate quickly we do this
first in notebook. In Jupyter, open `notebooks/validation.ipynb` and have a look at the validation put in place. We leave it up to the user to 
experiment and add some additional validation.

We will use the code of the notebook to write our first job. In VSCode or Jupyter, open `src/titanic/jobs/validate.py`. We have taken the code 
from our notebook, validated the schema and stored the output as a [parquet](https://parquet.apache.org/) file. Open `dags/titanic.py` and have a 
look at the `validate_task`. This describes how the code is called. 

You can test the code remotely by running `datafy run --env samples` and selecting the `validate_data` task. Another approach of testing and debugging the code is to call the code directly from the notebook. In Jupyter, open `notebooks/debug.ipynb` and run the the first few cells and
call the `run` function of the validate task.

#### Data preparation

Next, we will use the code from the `notebooks/model.ipynb` to create separate testable functions for each of the features we want to use. When you place close attention, you would see that the notebook is in fact already using the functions from the task we have created in `src/titanic/jobs/prepare.py`. After creating the features we split the dataset in a training and an evaluation set and store those for later use. Have a look at `dags/titanic.py` and the corresponding workflow task. 

To test the code we can run `datafy run --env samples` and select `prepare_data` or run the corresponding cells in `notebooks/debug.ipynb`. 

#### Model training

In this step we will use the output of the data preparation to train our model and store it so it can be used later on for model evaluation, model validation and inference. We used the model training code from `notebooks/model.ipynb` to create the task `src/titanic/jobs/training.py` with additional logic to load data and store the resulting model. We added a task to the workflow file `dags/titanic.py`.

To test the code we can run `datafy run --env samples` and select `train` or run the corresponding cells in `notebooks/debug.ipynb`. 


#### Model evalution

The last step we will cover in this ML pipeline is the evaluation. After loading the model and the evaluation data, we compare the predictions with the actuals and calculate the accuracy. We leave it up to the user to have a look at the corresponding files.

To test the code we can run `datafy run --env samples` and select `evaluate` or run the corresponding cells in `notebooks/debug.ipynb`.


#### Deployement

The different workflow tasks in `dags/titanic.py` are wired together. We are ready to deploy our pipeline:

1. `datafy build`
1. `datafy deploy --env samples --wait`
1. Navigate to `https://app.datafy.cloud/environments` and select the `samples` environment
1. Press the play button next to the `samples_titanic` dag in airflow to manually trigger the pipeline


#### Logs and metrics

Once your workflow was triggered you can inspect the logs and metrics of each task. 

1. Navigate to `https://app.datafy.cloud/environments` and select the `samples` environment
1. Select `Task executions`
1. Select any task to inspect the logs and metrics


#### Cleanup

1. `datafy notebook delete --env samples`
1. `datafy project delete`


### Conclusion

In this sample we have seen how we can use the notebook feature to analyse and experiment with data. Next we learned how to industrialize our code by creation small modular functions and integrating with the Airflow workflow manager. Last we covered the basics of building, deploying and running a project in an environment.