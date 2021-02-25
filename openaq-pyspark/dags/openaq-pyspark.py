from airflow import DAG
from airflow.operators.datafy_spark_plugin import DatafySparkSubmitOperator
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


image = "{{ macros.image('openaq-pyspark') }}"
role = "datafy-dp-{{ macros.env() }}/openaq-pyspark-{{ macros.env() }}"

dag = DAG(
    "openaq-pyspark",
    default_args=default_args,
    schedule_interval="@daily",
    max_active_runs=1,
)

load_openaq_data_task = DatafySparkSubmitOperator(
    dag=dag,
    task_id="load_openaq_data",
    num_executors="1",
    driver_instance_type='mx_micro',
    executor_instance_type='mx_micro',
    spark_main_version=3,
    env_vars={"AWS_REGION": "eu-west-1"},
    conf={
        "spark.kubernetes.container.image": image,
        "spark.kubernetes.driver.annotation.iam.amazonaws.com/role": role,
        "spark.kubernetes.executor.annotation.iam.amazonaws.com/role": role,
        "spark.sql.sources.partitionOverwriteMode": "dynamic"
    },
    application="local:///opt/spark/work-dir/src/openaq/app.py",
    application_args=["--date", "{{ ds }}", "--jobs", "sample", "--env", "{{ macros.env() }}"],
)
