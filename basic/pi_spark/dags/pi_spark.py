from airflow import DAG
from conveyor.operators import ConveyorSparkSubmitOperatorV2
from datetime import timedelta
from airflow.utils import dates

default_args = {
    "owner": "Conveyor",
    "depends_on_past": False,
    "start_date": dates.days_ago(2),
    "email": [],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "samples_pi_spark",
    default_args=default_args,
    schedule_interval="@daily",
    max_active_runs=1,
)
role = "conveyor-samples"

sample_task = ConveyorSparkSubmitOperatorV2(
    dag=dag,
    task_id="calculate_pi",
    num_executors="4",
    driver_instance_type="mx.medium",
    executor_instance_type="mx.medium",
    instance_life_cycle="spot",  # Other options are `on-demand`, `driver-on-demand-executors-spot`
    aws_role=role,
    spark_main_version=3,
    application="local:///opt/spark/work-dir/src/pi_spark/app.py",
    application_args=[
        "--date", "{{ ds }}",
        "--env", "{{ macros.conveyor.env() }}",
        "--partitions", "2000",
    ],
)
