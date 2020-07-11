from airflow import DAG
from airflow.operators.datafy_spark_plugin import DatafySparkSubmitOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "Datafy",
    "depends_on_past": False,
    "start_date": datetime(year=2020, month=6, day=22),
    "email": [],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}


image = "{{ macros.image('openaq-pyspark') }}"
role = "datafy-dp-{{ macros.env() }}/openaq-pyspark-{{ macros.env() }}"
hive_factory_class = (
    "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
)

dag = DAG(
    "openaq-pyspark",
    default_args=default_args,
    schedule_interval="@daily",
    max_active_runs=1,
)

executor_memory = "1G"
load_openaq_data_task = DatafySparkSubmitOperator(
    dag=dag,
    task_id="load_openaq_data",
    num_executors="1",
    executor_memory=executor_memory,
    driver_memory="512M",
    conn_id="spark-k8s",
    env_vars={"AWS_REGION": "eu-west-1"},
    conf={
        "spark.kubernetes.container.image": image,
        "spark.kubernetes.driver.annotation.iam.amazonaws.com/role": role,
        "spark.kubernetes.executor.annotation.iam.amazonaws.com/role": role,
        "spark.hadoop.hive.metastore.client.factory.class": hive_factory_class,
        "spark.sql.sources.partitionOverwriteMode": "dynamic"
    },
    application="/app/src/openaq/app.py",
    application_args=["--date {{ ds }}", "--jobs sample", "--env {{ macros.env() }}"],
)
