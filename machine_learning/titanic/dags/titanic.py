from airflow import DAG
from datafy.operators import DatafyContainerOperatorV2
from datetime import datetime, timedelta


default_args = {
    "owner": "Datafy",
    "depends_on_past": False,
    "start_date": datetime(year=2022, month=1, day=1),
    "email": [],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "titanic-training", default_args=default_args, schedule_interval=None, max_active_runs=1, is_paused_upon_creation=False
)
role = "datafy-samples"

validate_task = DatafyContainerOperatorV2(
    dag=dag,
    task_id="validate_data",
    instance_type='mx_nano',
    arguments=[
      "/app/src/titanic/jobs/validate.py",
      "--asset", "train",
      "--date", "{{ ds }}",
    ],
    aws_role=role,
)

prepare_task = DatafyContainerOperatorV2(
    dag=dag,
    task_id="prepare_data",
    instance_type='mx_nano',
    arguments=[
        "/app/src/titanic/jobs/prepare.py",
        "--asset", "train",
        "--date", "{{ ds }}",
    ],
    aws_role=role,
)

train_task = DatafyContainerOperatorV2(
    dag=dag,
    task_id="train",
    instance_type='mx_nano',
    arguments=[
        "/app/src/titanic/jobs/train.py",
        "--date", "{{ ds }}",
    ],
    aws_role=role,
)

evaluate_task = DatafyContainerOperatorV2(
    dag=dag,
    task_id="evaluate",
    instance_type='mx_nano',
    arguments=[
        "/app/src/titanic/jobs/evaluate.py",
        "--date", "{{ ds }}",
    ],
    aws_role=role,
)


validate_task >> prepare_task >> train_task >> evaluate_task
