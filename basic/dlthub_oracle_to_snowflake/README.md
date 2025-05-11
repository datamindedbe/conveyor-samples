# Oracle to Snowflake using dltHub

This project illustrates how one can extract data from an Oracle database and
load those into Snowflake using [dltHub][dlt]. Conveyor is used to facilitate
scheduling and deployment.

## Prerequisites

You will need to have some way to load data into an Oracle database. Scripts
generating demo data can be found online. For large datasets, consider
generating [TPC-H data][tpch] and loading it. This process will be explained
in the relevant section.

You will also need to have access to an AWS account where you are authorized
to setup an RDS instance and a secretsmanager.

Finally, you need access to a Snowflake environment. You need privileges to
create a role and grant it privileges.

### Infrastructure

1. Set up a small Oracle database and provision a Snowflake role.

   In this conveyor sample, we use [Hashicorp Terraform][tf] to create the
   required infrastructure, being:

   - an AWS RDS Oracle instance
     It is configured to load data from S3.

   Inside the infra folder of this sample, find the
   [aws_s3.tfbackend](./infra/aws_s3.tfbackend) file. Fill in the name to an
   existing AWS bucket you have access to using your AWS IAM role. You can
   modify the other settings as well, but likely won't need to.

   When you've filled in the missing details on where to store the Terraform
   state, navigate to the _infra_ folder in the shell and initialize the repo.

   ```sh
   cd infra
   terraform init -backend-config=aws_s3.tfbackend
   ```

   ⚠️ This process will also ask you for Snowflake credentials, so it can set
   up a role that will be required by dltHub to load data into schemas with.
   If you don't want to type these all the time, add them to a file called
   `snowflake_creds.tfvars`, which will be ignored by Git to prevent it from
   accidentally getting committed to your code repo.

   Next, apply the actual configuration:

   ```sh
   terraform apply
   ```

   The password to connect to the Oracle RDS instance will be retrievable in the
   secrets manager:

   ```sh
   aws secretsmanager list-secrets --filters 'Key=owning-service,Values=rds' --query 'SecretList[].Name'

   # pick the secret of interest from the output shown, and use it as the secret-id in the below command.

   aws secretsmanager get-secret-value --secret-id 'rds!db-6c34e3ce-1663-415f-81cf-e919fc50e7ca' --query SecretString | jq '. | fromjson'
   ```

2. Load that Oracle database with some data.

   Oracle comes with [its own demo schemas][oracle-demo-schemas], like the
   sales history (SH) schema, which may suffice for the demo. To allow more
   extensive benchmarks, you may be interested in the TPC-H benchmark data.
   To load that, you should first generate it using the _dbgen_ software that
   can be [downloaded from the TPC-H website][dbgen].

   When you've generated the data (e.g. using `dbgen -s 4`), upload it,
   gzipped, to an AWS S3 bucket. From there you can transfer it to the Oracle
   db's local storage:

   ```sql
   SELECT rdsadmin.rdsadmin_s3_tasks.download_from_s3(
     p_bucket_name => 'NAME OF THE BUCKET THAT CONTAINS THE DATA',
     p_directory_name => 'DATA_PUMP_DIR',
     p_s3_prefix => 'NAME OF THE FOLDER (well, S3 does not actually use
     folders, but prefixes) ON THE BUCKET THAT HOLDS THE DATA/',
     p_decompression_format => 'GZIP'
   ) AS TASK_ID FROM DUAL;
   ```

   This will launch an asynchronous task that you can monitor the progress of,
   as [explained in more details](https://docs.aws.amazon
   .com/AmazonRDS/latest/UserGuide/oracle-s3-integration.using.html) here.
   More importantly, this process allows you to see the errors that may occur (e
   .g. about missing access rights).

   Finally, you must declare the table schemas and
   [load the external data](https://seanstuber.com/2017/05/27/setting-up-tpc-h-test-data-with-oracle-on-linux/).

At this Extract data using a dlt pipeline.

## 🚀 Commands

We use [`uv`](https://github.com/astral-sh/uv) to manage Python dependencies efficiently. Here's how to get started:

### 🔧 Setup

1. [Install `uv`](https://github.com/astral-sh/uv?tab=readme-ov-file#installation)
2. **Install this project's dependencies:**

   This will automatically create a virtual environment as well.

   ```bash
   uv sync
   ```

   You might need some non-Python software as well, like clang. Install those using your operating system's tooling.

3. **Add new libraries during development:**

   ```bash
   uv add <library_name>
   ```

---

### ▶️ Running Pipelines

To run a specific pipeline script:

```bash
uv run <pipeline_file>.py
```

---

### 📊 Viewing Tables

To inspect the available tables in a pipeline:

```bash
dlt pipeline <pipeline_name> show
```

The `pipeline_name`s are given in [.dlt/config.toml](.dlt/config.toml).


## Required Infrastructure

setup & teardown


[dlt]: https://dlthub.com/
[tpch]: https://www.tpc.org/tpch/
[tf]: https://developer.hashicorp.com/terraform
[oracle-demo-schemas]: https://github.com/oracle-samples/db-sample-schemas
[dbgen]: https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp