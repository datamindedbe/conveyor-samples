# Alerting

In this example we use native airflow features to send notifications to Slack.

## Prerequisites

Before you can start this sample, you need to have access to a Slack workspace and be able to create a channel and an application with incoming webhook.

1. From your Slack workspace, create a channel you want to use to receive notification `conveyor-notifications`. The Slack documentation [here](https://slack.com/help/articles/201402297-Create-a-channel) walks you though it. 
1. From your Slack workspace, create a Slack app and an incoming Webhook. The Slack documentation [here](https://api.slack.com/messaging/webhooks) walks through the necessary steps. Take note of the Incoming Slack Webhook URL.


## Quickstart

1. Add the Incoming Slack Webhook URL as an HTTP connection to Airlow in the `samples` environment
1. Initialize this folder as a project: `conveyor project create --name samples_alerting`
1. Build the project: `conveyor build`
1. Deploy the project to the samples environment: `conveyor deploy --env samples --wait`
1. Run the created workflow:
    1. Navigate to `https://app.conveyordata.com/environments` and select the `samples` environment
    1. Enable the `samples_alerting_slack` and `samples_alerting_slack_sla` dag in airflow to start running the tasks on a daily basis
1. Check the slack channel for notifications


## Walkthrough

Navigate to this folder and initialize it as a conveyor project `conveyor project create --name samples_alerting`. Next we recommend opening the folder in VSCode


### Configuering Airflow

First we need to create an Airflow connection to provide your Incoming Slack Webhook URL to airflow. 

1. Navigate to `https://app.conveyordata.com/environments` and select the `samples` environment
1. Navigate to `Admin` > `Connections` in airflow
1. Add a connection of type HTTP
    1. Enter `slack_webhook` as the connection id
    1. Enter https://hooks.slack.com/services/ as the Host
    1. Enter the remainder of your Webhook URL as the Password (formatted as T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX)
1. Save


### Notification on failed DAG

Receiving notifications on failed tasks can lead to notification noise. One way to address this is by sending notifications 
when a DAG fails. This is done by defining the `on_failure_callback` in your DAG.

Have a look at the `dags/slack.py` file and more specifically at the function `slack_failed_dag_notification` and the `samples_alerting_slack` DAG.
Both tasks in this DAG will always fail and trigger the callback.


### Notification on missed SLA

Airflow SLAs (Service Level Agreements) are a type of notification that is triggered when tasks are taking longer than expected to complete. To set this on a DAG level, add the `sla` parameter to the `default_args` of the DAGs and by defining the `sla_miss_callback` in your DAG. Do note that SLAs are relative to the DAG execution date, not the task start time. 

Have a look at the `dags/slack.py` file and more specifically at the function `slack_sla_notification` and the `samples_alerting_slack_sla` DAG.
Both tasks in this DAG will sleep for 20 seconds while the SLA is defined at 30 seconds. This causes the missed SLA notifications to be triggered 
every time. 


### Deployement

1. `conveyor build`
1. `conveyor deploy --env samples --wait`
1. Navigate to `https://app.conveyordata.com/environments` and select the `samples` environment
1. Enable the `samples_alerting_slack` and `samples_alerting_slack_sla` dag in airflow to start running the tasks on a daily basis


### Cleanup

1. `conveyor project delete`


### Conclusion

In this sample we have seen how we can use native airflow features to send notifications to Slack when unexpected things happen.