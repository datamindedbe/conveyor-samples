from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.datafy_container_plugin import DatafyContainerOperator

default_args = {
    "owner": "Datafy",
    "depends_on_past": False,
    "start_date": datetime(year=2020, month=7, day=5),
    "email": [],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

image = "{{ macros.image('openaq-dbt') }}"

dag = DAG(
    "openaq-dbt", default_args=default_args, schedule_interval="@daily", max_active_runs=1
)

run = DatafyContainerOperator(
    dag=dag,
    task_id="run_dbt_models",
    name="run_dbt_models",
    image=image,
    env_vars={
        'TARGET': "{{ macros.env() }}",
        'DATE': "{{ ds }}"
    },
    service_account_name="openaq-dbt",
    cmds=["dbt"],
        arguments=[
            "run",
            "--target",
            "{{ macros.env() }}",
            "--profiles-dir",
            "."
        ],
)

test = DatafyContainerOperator(
    dag=dag,
    task_id="test_dbt_models",
    name="test_dbt_models",
    image=image,
    env_vars={
        'TARGET': "{{ macros.env() }}",
        'DATE': "{{ ds }}"
    },
    service_account_name="openaq-dbt",
    cmds=["dbt"],
        arguments=[
            "test",
            "--target",
            "{{ macros.env() }}",
            "--profiles-dir",
            "."
        ],
)

run >> test
