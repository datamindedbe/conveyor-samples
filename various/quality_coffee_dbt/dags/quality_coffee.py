from datetime import timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.utils import dates

from conveyor.operators import ConveyorContainerOperatorV2

in_production = "prd" in Variable.get("environment")

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
    "samples_quality_coffee",
    default_args=default_args,
    schedule_interval="@daily",
    max_active_runs=1,
)

staging = ConveyorContainerOperatorV2(
    dag=dag,
    task_id="staging",
    aws_role="conveyor-samples",
    arguments=[
        "run",
        "--target", "dev",
        "--select", "staging",
    ],
)

marts = ConveyorContainerOperatorV2(
    dag=dag,
    task_id="marts",
    aws_role="conveyor-samples",
    arguments=[
        "run",
        "--target", "dev",
        "--select", "marts",
    ],
)

staging >> marts

if in_production:
    # Tasks that should only be present in production
    pass
