from airflow import DAG
from conveyor.operators import ConveyorContainerOperatorV2
from datetime import timedelta
import pendulum

default_args = {
    "owner": "Conveyor",
    "depends_on_past": False,
    "start_date": pendulum.datetime(2025, 4, 22, tz="Europe/Brussels"),
    "email": [],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "samples_sqlmesh",
    default_args=default_args,
    schedule_interval=timedelta(hours=3),
    max_active_runs=1,
    end_date=pendulum.datetime(2025, 4, 25),
)

sample_task = ConveyorContainerOperatorV2(
    dag=dag,
    task_id="samples_sqlmesh",
    aws_role="conveyor-samples",
)