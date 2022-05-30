from airflow import DAG
from airflow.models import Variable
from airflow.providers.slack.operators.slack_webhook import SlackWebhookHook
from conveyor.operators import ConveyorContainerOperatorV2
from datetime import datetime, timedelta


def slack_failed_dag_notification(context):
    environment = Variable.get("environment", "unknown")
    slack_msg = """
            :red_circle: DAG `{dag}` in environment `{env}` failed. 
            *DAG*: {dag}
            *Environment*: {env}
            *Execution Time*: {exec_date}
            *Reason*: {reason}
            *Url*: https://app.conveyordata.com/environments/{env}/airflow/tree?dag_id={dag}
            """.format(
            dag=context.get('dag_run').dag_id,
            env=environment,
            exec_date=context.get('execution_date'),
            reason=context.get('reason'),
        )
    hook = SlackWebhookHook(
        http_conn_id="slack_webhook",
        message=slack_msg,
    )
    hook.execute()


default_args = {
    "owner": "Conveyor",
    "depends_on_past": False,
    "start_date": datetime(year=2022, month=1, day=1),
    "email": [],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

dag_failed = DAG(
    "samples_alerting_slack",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    max_active_runs=1,
    on_failure_callback=slack_failed_dag_notification
)

ConveyorContainerOperatorV2(
    dag=dag_failed,
    task_id="sample_failing",
    cmds=["python"],
    arguments=["-m", "alerting.sample_fail", "--date", "{{ ds }}", "--env", "{{ macros.conveyor.env() }}"],
    instance_type="mx.micro",
    aws_role="samples_slack-{{ macros.conveyor.env() }}",
)

ConveyorContainerOperatorV2(
    dag=dag_failed,
    task_id="sample_failing_2",
    cmds=["python"],
    arguments=["-m", "alerting.sample_fail", "--date", "{{ ds }}", "--env", "{{ macros.conveyor.env() }}"],
    instance_type="mx.micro",
    aws_role="samples_slack-{{ macros.conveyor.env() }}",
)

def slack_sla_notification(dag, task_list, blocking_task_list, slas, blocking_tis, *args, **kwargs):
    environment = Variable.get("environment", "unknown")
    slack_msg = """
            :red_circle: DAG `{dag}` in environment `{env}` missed SLA. 
            *DAG*: {dag}
            *Environment*: {env}
            *Execution Time*: {exec_date}
            *Tasks*: {tasks}
            *Blocking tasks*: {blocking}
            *Url*: https://app.conveyordata.com/environments/{env}/airflow/tree?dag_id={dag}
            """.format(
            dag=slas[0].dag_id,
            env=environment,
            exec_date=slas[0].execution_date.isoformat(),
            tasks=task_list,
            blocking=blocking_task_list,
        )
    hook = SlackWebhookHook(
        http_conn_id="slack_webhook",
        message=slack_msg,
    )
    hook.execute()


dag_sla = DAG(
    "samples_alerting_slack_sla",
    default_args={**default_args, 'sla': timedelta(seconds=30)},
    schedule_interval="@daily",
    catchup=False,
    max_active_runs=1,
    sla_miss_callback=slack_sla_notification
)

sample_sla = ConveyorContainerOperatorV2(
    dag=dag_sla,
    task_id="sample_sla",
    cmds=["python"],
    arguments=["-m", "alerting.sample_sla", "--date", "{{ ds }}", "--env", "{{ macros.conveyor.env() }}"],
    instance_type="mx.micro",
    aws_role="samples_slack-{{ macros.conveyor.env() }}",
)

sample_sla_2 = ConveyorContainerOperatorV2(
    dag=dag_sla,
    task_id="sample_sla_2",
    cmds=["python"],
    arguments=["-m", "alerting.sample_sla", "--date", "{{ ds }}", "--env", "{{ macros.conveyor.env() }}"],
    instance_type="mx.micro",
    aws_role="samples_slack-{{ macros.conveyor.env() }}",
)

sample_sla >> sample_sla_2
