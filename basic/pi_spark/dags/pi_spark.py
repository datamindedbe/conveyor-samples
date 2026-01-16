from airflow import DAG
from conveyor.operators import ConveyorSparkSubmitOperatorV2
from datetime import timedelta, datetime
from airflow.utils import dates

default_args = {
    "owner": "Conveyor",
    "depends_on_past": False,
    "email": [],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "start_date": datetime(year=2026, month=1, day=5),
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "samples_pi_spark",
    default_args=default_args,
    schedule="@daily",
    max_active_runs=1,
)
role = "conveyor-samples"

ConveyorSparkSubmitOperatorV2(
    dag=dag,
    task_id="calculate_pi",
    num_executors=2,
    driver_instance_type="mx.medium",
    executor_instance_type="cx.xlarge",
    instance_life_cycle="spot",  # Other options are `on-demand`, `driver-on-demand-executors-spot`
    aws_role=role,
    spark_main_version=3,
    application="local:///opt/spark/work-dir/src/pi_spark/app.py",
    application_args=[
        "--date", "{{ ds }}",
        "--env", "{{ macros.conveyor.env() }}",
        "--partitions", "1000",
        "--iterations", "3000000000",
    ],
)


ConveyorSparkSubmitOperatorV2(
    dag=dag,
    task_id="calculate_pi_inefficient",
    num_executors=1,
    driver_instance_type="mx.medium",
    executor_instance_type="cx.xlarge",
    instance_life_cycle="spot",  # Other options are `on-demand`, `driver-on-demand-executors-spot`
    aws_role=role,
    spark_main_version=3,
    application="local:///opt/spark/work-dir/src/pi_spark/app.py",
    application_args=[
        "--date", "{{ ds }}",
        "--env", "{{ macros.conveyor.env() }}",
        "--partitions", "3",
        "--iterations", "3000000000",
    ],
)
