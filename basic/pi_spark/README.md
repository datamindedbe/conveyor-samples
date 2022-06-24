# Pi Spark

In this example we use distributed engine Spark to calculate Pi. 


## Quickstart

1. Initialize this folder as a project: `conveyor project create --name samples_pi_spark`
1. Build the project: `conveyor build`
1. Deploy the project to the samples environment: `conveyor deploy --env samples --wait`
1. Run the created workflow:
    1. Navigate to `https://app.conveyordata.com/environments` and select the `samples` environment
    1. Enable the `samples_pi_spark` dag in airflow to start running the tasks on a daily basis
1. Cleanup after using `conveyor project delete`


