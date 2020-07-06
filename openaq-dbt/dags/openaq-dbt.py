from airflow import DAG
from airflow.operators.datafy_container_plugin import DatafyContainerOperator
from datetime import datetime, timedelta


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

DatafyContainerOperator(
    dag=dag,
    task_id="sample",
    name="sample",
    image=image,
    arguments=["--date", "{{ ds }}", "--jobs", "sample", "--env", "{{ macros.env() }}"],
    service_account_name="openaq-dbt"
)
