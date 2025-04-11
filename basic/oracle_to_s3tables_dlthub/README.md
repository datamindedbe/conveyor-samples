# Context

This is a sample to illustrate how one can extract data from an Oracle database and load those into S3 Tables.

V1 will have the extraction from Oracle to the local file system.
In V2, the local file system will be replaced with S3 Tables.

## V1

1. Set up a small Oracle database.

   Run `cd infra && terraform apply`. The password to connect to the Oracle instance will be retrievable in the secrets manager:

   ```sh
   aws secretsmanager list-secrets --filters 'Key=owning-service,Values=rds' --query 'SecretList[].Name'

   # pick the secret of interest from the output shown, and use it as the secret-id in the below command.

   aws secretsmanager get-secret-value --secret-id 'rds!db-6c34e3ce-1663-415f-81cf-e919fc50e7ca' --query SecretString | jq '. | fromjson'

   ```

2. Load that Oracle database with some data.

   Oracle comes with its own demo schemas, like SH, which are fairly small but get generated from (long) sql files. We'll be using TPC-H though to allow benchmarking and have data of a certain size.

   Data is uploaded to _s3://tcph-100gb/_. There's both a 4GB (`dbgen -s 4`) and a 100GB version (`dbgen -s 100`).

   Once the data is there, you need to transfer it to the Oracle db's local storage, which can be done with:

   ```sql
   SELECT rdsadmin.rdsadmin_s3_tasks.download_from_s3(
     p_bucket_name => 'tcph-100gb',
     p_directory_name => 'DATA_PUMP_DIR',
     p_s3_prefix => '4GB/',
     p_decompression_format => 'GZIP'
   ) AS TASK_ID FROM DUAL;
   ```

   which will launch an asynchronous task that you can monitor the progress of,
   as [explained in more details](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/oracle-s3-integration.using.html) here. More importantly, it allows you to see the errors that may occur (e.g. about missing access rights)

   Finally, you must declare the table schemas and
   [load the external data](https://seanstuber.com/2017/05/27/setting-up-tpc-h-test-data-with-oracle-on-linux/).

3. Extract data using a dlt pipeline.

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
python <pipeline_file>.py
```

---

### 📊 Viewing Tables

To inspect the available tables in a pipeline:

```bash
dlt pipeline <pipeline_name> show
```

The `pipeline_name`s are given in [.dlt/config.toml](.dlt/config.toml).