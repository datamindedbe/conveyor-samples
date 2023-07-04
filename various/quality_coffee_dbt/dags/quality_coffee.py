from datetime import timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.utils import dates

from conveyor.operators import ConveyorContainerOperatorV2
from conveyor.secrets import AWSParameterStoreValue

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

def dbt_task(*, task_id: str, arguments: list[str]) -> ConveyorContainerOperatorV2:
    return ConveyorContainerOperatorV2(
        dag=dag,
        task_id=task_id,
        aws_role="conveyor-samples",
        env_vars={
            "POSTGRES_HOST": AWSParameterStoreValue(name="/conveyor-samples/postgres_host"),
            "POSTGRES_PASSWORD": AWSParameterStoreValue(name="/conveyor-samples/postgres_password"),
        },
        arguments=arguments,
    )

staging = dbt_task(task_id="staging", arguments=["run", "--select", "staging"])
marts = dbt_task(task_id="marts", arguments=["run", "--select", "marts"])

staging >> marts

if not in_production:
    # Tasks that should not be present in production
    seed = dbt_task(task_id="seed", arguments=["seed"])
    seed >> staging
