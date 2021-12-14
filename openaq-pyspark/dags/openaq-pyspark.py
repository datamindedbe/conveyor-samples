from airflow import DAG
from datafy.operators import DatafySparkSubmitOperatorV2
from datetime import timedelta
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

role = "openaq-pyspark-{{ macros.datafy.env() }}"

dag = DAG(
    "openaq-pyspark",
    default_args=default_args,
    schedule_interval="@daily",
    max_active_runs=1,
)

load_openaq_data_task = DatafySparkSubmitOperatorV2(
    dag=dag,
    task_id="load_openaq_data",
    num_executors="1",
    executor_instance_type='mx_medium',
    spark_main_version=3,
    aws_role=role,
    conf={
        "spark.sql.sources.partitionOverwriteMode": "dynamic"
    },
    application="local:///opt/spark/work-dir/src/openaq/sample.py",
    application_args=["--date", "{{ ds }}", "--env", "{{ macros.datafy.env() }}"],
)
