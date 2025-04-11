from airflow import DAG
from conveyor.operators import ConveyorContainerOperatorV2
from datetime import timedelta
import pendulum

default_args = {
    "owner": "Conveyor",
    "depends_on_past": False,
    "start_date": pendulum.datetime(2025, 4, 10, tz="Europe/Brussels"),
    "email": [],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "oracle2local",
    default_args=default_args,
    schedule_interval="@daily",
    max_active_runs=1,
)
role = "conveyor-samples"

sample_task = ConveyorContainerOperatorV2(
    dag=dag,
    task_id="calculate_pi",
    instance_type="mx.nano",
    aws_role="",
)
