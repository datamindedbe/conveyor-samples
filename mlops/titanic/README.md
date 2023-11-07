# Titanic

In this example, we use the dataset from [Kaggle](https://www.kaggle.com/c/titanic) to build an ML model that can be used to predict survival on the Titanic. 
We move from experiment to industrialization and cover the steps of data analysis, data preparation, model training and model evaluation. 

## Prerequisites

### Data

Before you can start this sample, you need to copy the data from Kaggle to the S3 bucket created as a prerequisite.

1. Open https://www.kaggle.com/ and login or register (it's free)
2. Navigate to https://www.kaggle.com/c/titanic and download the `test.csv` and `train.csv` in the data tab
3. Copy both files to the `conveyor-samples-*` s3 bucket under `titanic/raw`. You can use either the AWS Console or the AWS CLI.

```bash
aws s3 cp test.csv s3://conveyor-samples-*/titanic/raw/test.csv
aws s3 cp test.csv s3://conveyor-samples-*/titanic/raw/train.csv
```

## Quickstart

1. Initialize this folder as a project: `conveyor project create --name samples_titanic`
2. Build the project: `conveyor build`
3. Deploy the project to the samples environment: `conveyor deploy --env samples --wait`
4. Run the created workflow:
    1. Navigate to `https://app.conveyordata.com/environments` and select the `samples` environment
    2. Press the play button next to the `samples_titanic_training` dag in airflow to manually trigger the pipeline


## Walkthrough

Navigate to this folder and initialize it as a conveyor project `conveyor project create --name samples_titanic`.
Next, we recommend opening the folder in a Conveyor IDE.

If you're exploring this project in the Conveyor Playground,
chances are you've already opened this project in an IDE, and are now reading this file there.
In this case, you won't need to create any new project or IDE.

### Experiment

#### Data analysis

First, we explore and analyse the data.
To do this, we use the notebook support provided by Conveyor IDEs.
If you're running this sample in your own Conveyor environment, execute `conveyor ide create --env samples`.
This will package the code, publish it and start a new IDE instance that will open in your browser window.
This might take a while the first time.
In the IDE, you can open `notebooks/exploration.ipynb` and it will render this as a Jupyter notebook.
Execute the cells in the notebook and see how we used this to gain a better understanding of the data.

We don't take credit for this effort. All thanks goes to https://medium.com/analytics-vidhya/exploratory-data-analysis-of-titanic-survival-problem-e3af0fb1f276.

#### Building a first model

The next step is to find a first suitable model.
In the Conveyor IDE, open `notebooks/model.ipynb`.
Execute the cells in the notebook and see how we use our understanding of the data done in the previous step,
to build features, evaluate their importance and try a number of models.

Once we find a model that is good enough, we can start the automation process.

### Industrialization

As described by Google as [MLOps](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) we will automate a pipeline that consists of: 

1. data validation
2. data preparation
3. model training
4. model evaluation

For the sake of simplicity, we will not cover the step of model validation in this sample.

#### Data validation

In this step, we will use the [pandera](https://pandera.readthedocs.io/en/stable/) library to validate our data.
To iterate quickly, we do this first in notebook.
In the Conveyor IDE, open `notebooks/validation.ipynb` and have a look at the validation put in place.
We leave it up to the user to experiment and add some additional validation.

We will use the code of the notebook to write our first job.
Please have a look at `src/titanic/jobs/validate.py`.
We have taken the code from our notebook,
validated the schema and stored the output as a [parquet](https://parquet.apache.org/) file.

Next, open `dags/titanic.py` and have a look at the `validate_task`.
This describes how the code is called when run on Airflow.

You can test the code remotely by running `conveyor run --env samples` and selecting the `validate_data` task.
Another approach of testing and debugging the code is to call the code directly from the notebook.
In the Conveyor IDE, open `notebooks/debug.ipynb` and run the first few cells and call the `run` function of the validate task.

#### Data preparation

Next, we will use the code from the `notebooks/model.ipynb` to create separate testable functions for each of the features we want to use.
When you place close attention, you would see that the notebook is in fact already using the functions from the task we have created in `src/titanic/jobs/prepare.py`.
After creating the features, we split the dataset in a training and an evaluation set and store those for later use.
Have a look at `dags/titanic.py` and the corresponding workflow task. 

To test the code we can run `conveyor run --env samples` and select `prepare_data` or run the corresponding cells in `notebooks/debug.ipynb`. 

#### Model training

In this step, we will use the output of the data preparation to train our model and store it so it can be used later on for model evaluation, model validation, and inference.
We used the model training code from `notebooks/model.ipynb` to create the task `src/titanic/jobs/training.py` with additional logic to load data and store the resulting model.
We added a task to the workflow file `dags/titanic.py`.

To test the code we can run `conveyor run --env samples` and select `train` or run the corresponding cells in `notebooks/debug.ipynb`. 

#### Model evaluation

The last step we will cover in this ML pipeline is the evaluation.
After loading the model and the evaluation data, we compare the predictions with the actuals and calculate the accuracy.
We leave it up to the user to have a look at the corresponding files.

To test the code we can run `conveyor run --env samples` and select `evaluate` or run the corresponding cells in `notebooks/debug.ipynb`.

#### Deployment

The different workflow tasks in `dags/titanic.py` are wired together. We are ready to deploy our pipeline:

1. `conveyor build`
2. `conveyor deploy --env samples --wait`
3. Navigate to `https://app.conveyordata.com/environments` and select the `samples` environment
4. Press the play button next to the `samples_titanic_training` dag in Airflow to manually trigger the pipeline

#### Logs and metrics

Once your workflow is triggered, you can inspect the logs and metrics of each task. 

1. Navigate to `https://app.conveyordata.com/environments` and select the `samples` environment
2. Select `Task executions`
3. Select any task to inspect the logs and metrics

#### Cleanup

In case you're not running this on the Conveyor playground and want to clean up the Conveyor resources you've created,
you can run the following commands:

1. `conveyor notebook delete --env samples`
2. `conveyor project delete`

### Conclusion

In this sample, we have seen how we can use the notebook feature of the Conveyor IDE to analyse and experiment with data.
Next, we learned how to industrialize our code by creating small modular functions and integrating with the Airflow workflow manager.
Last, we covered the basics of building, deploying and running a project in a Conveyor environment.
