# Pi Spark

In this example, we use distributed engine Spark to calculate Pi. 

## Playground

If you're looking at this in the Conveyor Playground,
everything will already be initialized, and you don't need to follow the Quickstart below.

Just have a look at the code and explore the capabilities!

## Quickstart

1. Initialize this folder as a project: `conveyor project create --name samples_pi_spark`
2. Build the project: `conveyor build`
3. Deploy the project to the samples environment: `conveyor deploy --env samples --wait`
4. Run the created workflow:
    1. Navigate to `https://app.conveyordata.com/environments` and select the `samples` environment.
    2. Enable the `samples_pi_spark` dag in Airflow to start running the tasks on a daily basis.
5. Cleanup after using `conveyor project delete`
