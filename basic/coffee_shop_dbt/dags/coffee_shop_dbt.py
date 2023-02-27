from airflow import DAG
from conveyor.factories import ConveyorDbtTaskFactory
from conveyor.operators import ConveyorContainerOperatorV2
from datetime import datetime, timedelta
from airflow.utils import dates


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
    "samples_coffee_shop_dbt", default_args=default_args, schedule_interval="@daily", max_active_runs=1
)

staging = ConveyorContainerOperatorV2(
    dag=dag,
    task_id="staging",
    aws_role="conveyor-samples",
    arguments=["run", "--target", "dev", "-s", "staging"],
)

marts = ConveyorContainerOperatorV2(
    dag=dag,
    task_id="marts",
    aws_role="conveyor-samples",
    arguments=["run", "--target", "dev", "-s", "marts"],
)

staging >> marts

dag2 = DAG(
    "samples_coffee_shop_dbt_factory", default_args=default_args, schedule_interval="@daily", max_active_runs=1
)

factory = ConveyorDbtTaskFactory(task_aws_role="conveyor-samples",
)
start, end = factory.add_tasks_to_dag(dag=dag2)

