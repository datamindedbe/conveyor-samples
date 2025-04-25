# Context

This sample shows how to transform data in Snowflake using SQLMesh. Here we use the TPCH data in the `SNOWFLAKE_SAMPLE_DATA` database. For the proposal of ***Conveyor and SQLMesh's Write-Audit-Publish pattern***, please refer to [here](./docs/README.md).

## Environment Setup

We use [`uv`](https://github.com/astral-sh/uv) to manage Python dependencies efficiently. 

1. [Install `uv`](https://github.com/astral-sh/uv?tab=readme-ov-file#installation).

2. **Install this project's dependencies:**

   This will automatically create a virtual environment as well.

   ```bash
   uv sync
   ```

3. **Add new libraries during development:**

   ```bash
   uv add <library_name>
   ```

## Snowflake Setup

We have set up snowflake access control permissions using Terraform. The terraform files are in the `infra` directory, following the [queries](./docs/snowflake.sql) suggested by the SQLMesh documentation. The terraform states files are stored to DM s3 bukect.

## Configuration Setup

Please copy paste the `config.yaml.template` file and rename it as `config.yaml`. 

We use a service user `sqlmesh_demo_user` for the default gateway, please consult Oliver or Siyan for the password, or change the password by re-applying terraform. To do that, you just need to provide a new value for the `snowflake_password` variable. 

If you want to use the `snowflake-interactive` gateway, which use your own DM account to authenticate snowflake via sso, you need to ensure you have access to the Snowflake playground account first and grant more permissions to your user. This is not recommended here.

## Running the Project

To run the project:

```bash
uv run sqlmesh plan <env>
```

The `<env>` is default to `prod` if omitted.

## SQLMesh Virtual Environment

SQLMesh is featured with [virtual data environment](https://www.tobikodata.com/blog/virtual-data-environments). 

For example, running:

```bash
uv run sqlmesh plan my_dev
```

Creates a schema suffixed with `__my_dev`, containing only the updated views.

To include views for all models (including unmodified ones), use the `--include-unmodified` flag:

```bash
uv run sqlmesh plan my_dev --include-unmodified
```

## SQLMesh integration with DLT

To integrate SQLMesh with `dlt`, refer to the official [integration documentation](https://sqlmesh.readthedocs.io/en/stable/integrations/dlt).