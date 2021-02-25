from datetime import timedelta

from airflow import DAG
from airflow.operators.datafy_container_plugin import DatafyContainerOperator
from airflow.operators.sensors import ExternalTaskSensor
from airflow.utils.dates import days_ago

default_args = {
    "owner": "Datafy",
    "depends_on_past": False,
    "start_date": days_ago(2),
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

wait_for_openaq_data = ExternalTaskSensor(
    dag=dag,
    task_id='wait_for_openaq_data',
    external_dag_id='openaq-pyspark',
    external_task_id='load_openaq_data'
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
    instance_type='mx_micro',
    service_account_name="openaq-dbt",
    cmds=["dbt"],
    arguments=[
        "run",
        "--target",
        "dev",
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
    instance_type='mx_micro',
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

wait_for_openaq_data >> run >> test
