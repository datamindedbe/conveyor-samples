# Context

This sample shows how to transform data in Snowflake using SQLMesh. Here we use the TPCH data in `SNOWFLAKE_SAMPLE_DATA` database. For the proposal of ***Conveyor and SQLMesh's Write-Audit-Publish pattern***, please refer to [here](./docs/README.md).

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

We have set up snowflake access control permissions using Terraform. The terraform files are in the `infra` directory, following the [queries](./docs/snowflake.sql) suggested in SQLMesh documentations. In case you want to make any changes, please input the `snowflake_username` as your DM email address and authenticate via sso.

## Configuration Setup

Please copy paste the `config.yaml.template` file and rename it as `config.yaml`. We use a service user `sqlmesh_demo_user` for the default gateway, please consult Oliver or Siyan for the password, or change the password by re-applying terraform. To do that, you just need to provide another password for `snowflake_password`. If you want to use the `snowflake-interactive` gateway, which use your own DM account to authenticate snowflake via sso, you need to ensure you have access to the Snowflake playground account first and grant more permissions to your user. This is not recommended here.

## Running the Project

To run the project:

```bash
uv run sqlmesh plan <env>
```

The env is default to `prod` if omitted.