from airflow import DAG
from conveyor.factories import ConveyorDbtTaskFactory
from conveyor.operators import ConveyorContainerOperatorV2
from datetime import datetime, timedelta


default_args = {
    "owner": "Conveyor",
    "depends_on_past": False,
    "start_date": datetime(year=2023, month=2, day=20),
    "email": [],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}


dag = DAG(
    "coffee_shop_dbt", default_args=default_args, schedule_interval="@daily", max_active_runs=1
)

ConveyorContainerOperatorV2(
    dag=dag,
    task_id="staging",
    aws_role="coffee_shop_dbt-{{ macros.conveyor.env() }}",
    arguments=["run", "--target", "dev"],
)
