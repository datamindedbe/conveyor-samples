# SQLMesh Snowflake Example

This sample demonstrates transforming data in Snowflake using [SQLMesh](https://sqlmesh.readthedocs.io/en/stable/).

## Prerequisites

Before you start, make sure you have the following:

*   **`uv`:** We use [`uv`](https://github.com/astral-sh/uv) for Python environment and dependency management. Follow their [installation guide](https://github.com/astral-sh/uv?tab=readme-ov-file#installation). This is needed for local development and understanding the project before using Conveyor.
*   **Terraform:** Required for setting up the necessary Snowflake infrastructure if you run or adapt the `infra` code. [Install Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).
*   **Snowflake Account:** Access to a Snowflake account where you (or the Conveyor environment) can create resources.

### Infra

This sample includes Terraform code (`infra/`) to set up the required Snowflake resources: a database (`SQLMESH_DEMO_DB`), a role (`SQLMESH`), a service user (`sqlmesh_demo_user`), and a warehouse (`COMPUTE_WH`).

1.  **Navigate to the `infra` directory:**
    ```bash
    cd infra
    ```
2.  **Create Terraform Variables File:**
    *   Copy the sample variables file: `cp sample.tfvars terraform.tfvars`
    *   Edit `terraform.tfvars` and provide your Snowflake details
3.  **Initialize Terraform:**
    ```bash
    terraform init
    ```
4.  **Apply Terraform:** Terraform will connect using your personal Snowflake user (specified in `terraform.tfvars`) to create the resources. You might be prompted for your personal Snowflake password or need to configure the [Snowflake Terraform provider](https://registry.terraform.io/providers/Snowflake-Labs/snowflake/latest/docs#authentication) appropriately (e.g., using environment variables, key pair authentication).
    ```bash
    terraform apply
    ```


### Data

1.  **TPCH Sample Data:** This project uses the standard `SNOWFLAKE_SAMPLE_DATA` database available in Snowflake. Ensure this database is available and accessible within your Snowflake account. The Terraform setup (if used) grants the `SQLMESH` role usage on this database.

## Quickstart 

These commands assume you are in the root directory of the `sqlmesh_example` project and want to run this sample using Conveyor in a `samples` environment.

1.  **Initialize Conveyor Project:**
    ```bash
    conveyor project create --name samples_sqlmesh_example
    ```
2.  **Build the Project:** Packages the code and dependencies.
    ```bash
    conveyor build
    ```
3.  **Deploy to Samples Environment:** Deploys the packaged code and any associated DAGs to the Conveyor `samples` environment.
    ```bash
    conveyor deploy --env samples --wait
    ```

4. Run the created workflow:
    1. Navigate to `https://app.conveyordata.com/environments` and select the `samples` environment
    2. Press the play button next to the `samples_sqlmesh` dag in airflow to manually trigger the pipeline


5.  **Cleanup (Conveyor):** Remove the deployed Conveyor project resources.
    ```bash
    conveyor project delete --name samples_sqlmesh_example --force
    ```

## Walkthrough

This sample project demonstrates a basic data transformation pipeline using SQLMesh with Snowflake. We'll first explore how to run it locally using `uv` and then show how to package and run it using Conveyor.

### Local Development 

This is useful for iterating on the SQLMesh models and logic before deploying with Conveyor. See the [SQLMesh Project Structure Guide](https://sqlmesh.readthedocs.io/en/stable/guides/project_structure/overview/) for details on `models/`, `audits/`, etc.

1.  **Prerequisites:** Ensure you have completed the setup steps in the [Prerequisites](#prerequisites) section (uv, Terraform Apply (recommended for local testing)).
2.  **Set up sqlmesh configuration file:** For local development, SQLMesh needs a `config.yaml` file to define connections to Snowflake.
    *   Copy the template: `cp config.yaml.template config.yaml`
    *   Edit `config.yaml`:
        *   Locate the `gateways:` -> `snowflake:` -> `connection:` section.
        *   Update `account:` with your full Snowflake account locator (e.g., `orgname-accountname.snowflakecomputing.com` or `xy12345.eu-central-1.aws`). You can derive parts of this from the `organization_name` and `account_name` used in `terraform.tfvars`.
        *   Update `password`, `warehouse`, `database`, with the exact values you provided in your `terraform.tfvars` file 
    *   The `snowflake-interactive` gateway example is provided for optional SSO-based local development but is commented out by default.
    *   See the [SQLMesh Configuration Guide](https://sqlmesh.readthedocs.io/en/stable/guides/configuration/project_configuration/) for more details on configuring gateways.

3.  **Install Dependencies:** Run `uv sync` in the project root. This creates a local virtual environment (`.venv`) and installs `sqlmesh`, `snowflake-connector-python`, etc.
4.  **Plan Production Environment:** The core SQLMesh command is [`sqlmesh plan [environment]`](https://sqlmesh.readthedocs.io/en/stable/reference/cli/#plan). Running `uv run sqlmesh plan prod` (or just `uv run sqlmesh plan`) analyzes your models (`models/`) against the target Snowflake database defined in your local `config.yaml`.
    *   SQLMesh compares local definitions to the recorded state for the `prod` environment.
    *   It lists models needing backfill (initial population) and runs tests.
5.  **Apply Production Plan:** When prompted `Apply - Backfill Tables [y/n]:`, type `y`. SQLMesh connects to Snowflake using your local `config.yaml` credentials and executes the SQL to build your models in the `prod` SQLMesh environment (typically within your `SQLMESH_DEMO_DB` database). Learn more about [Plans and Environments](https://sqlmesh.readthedocs.io/en/stable/concepts/plans/).
6.  **Explore Development Environments:** Make a change to a model (e.g., `models/staging/stg_orders.sql`). Run `uv run sqlmesh plan my_dev`. SQLMesh plans the creation of a *new* isolated schema (e.g., `SQLMESH_DEMO_DB__MY_DEV`). Apply the plan (`y`). This allows safe testing using [SQLMesh Environments](https://sqlmesh.readthedocs.io/en/stable/concepts/environments/). You can query this `__my_dev` schema in Snowflake.
7.  **Promote to Production (Locally):** Once changes are validated in `my_dev`, run `uv run sqlmesh plan prod` again. Apply the plan (`y`). SQLMesh efficiently promotes the changes to the `prod` environment, potentially via a quick "Virtual Update".
8.  **Run for New Intervals:** Use [`sqlmesh run prod`](https://sqlmesh.readthedocs.io/en/stable/reference/cli/#run) to evaluate models based on their schedules (`cron`) or process newly arrived data intervals.

### Running with Conveyor

Conveyor takes your local SQLMesh project, packages it into a container, and runs it in a managed environment, typically using Airflow for orchestration based on the DAGs in the `dags/` folder.

1.  **Initialize Conveyor Project:** `conveyor project create --name samples_sqlmesh_example` associates this local directory with a Conveyor project name.
2.  **Build:** `conveyor build` uses the `Dockerfile` to create a container image containing your SQLMesh project code and dependencies. It pushes this image to Conveyor's registry.
3.  **Deploy:** `conveyor deploy --env samples --wait` deploys the built image and the Airflow DAG (`dags/sqlmesh_dag.py`) to the specified Conveyor environment (e.g., `samples`). Conveyor automatically manages connections based on the environment's configuration, usually overriding the local `config.yaml`.
4.  **Trigger the Pipeline:**
    *   **Via `conveyor run`:** As shown in the Quickstart, `conveyor run task --env samples sqlmesh_plan_apply_prod --wait` directly triggers a specific task (like applying the 'prod' plan) defined within your deployed Airflow DAG. This task executes the `sqlmesh plan prod --auto-apply` command within the container running in Conveyor. The [`--auto-apply`](https://sqlmesh.readthedocs.io/en/stable/reference/cli/#cmdoption-arg-sqlmesh-plan-auto-apply) flag skips the interactive confirmation.
    *   **Via Airflow UI:** Navigate to your Conveyor `samples` environment's Airflow UI. Find the `samples_sqlmesh_example` DAG and trigger it manually. This will run the defined pipeline (e.g., plan+apply, potentially run).
5.  **Verify in Conveyor:**
    *   Check the logs of the Airflow tasks in the Conveyor UI (`Task Executions`) to see the output of the `sqlmesh` commands.
    *   Connect to your Snowflake instance and check the schemas/tables managed by SQLMesh, noting that they might be in a different database or schema controlled by the Conveyor `samples` environment's service account, depending on its configuration.

### Verification

After running the SQLMesh pipeline either locally or via Conveyor, you can verify the results in Snowflake:

1.  **Connect to Snowflake:** Use your preferred SQL client or the Snowflake UI. Connect to the account specified during the setup (e.g., in `terraform.tfvars`).
2.  **Locate the Database:** Navigate to the database created by the Terraform script (default is `SQLMESH_DEMO_DB`). This is where SQLMesh manages its objects.
3.  **Identify Schemas:** SQLMesh organizes tables within schemas inside the target database:
    *   **Production Environment (`prod`):** Tables for the `prod` environment are typically placed in a schema reflecting the project's configuration. Based on the Terraform setup, this is likely the `SQLMESH` schema (corresponding to the role). Look for tables like `SQLMESH_DEMO_DB.SQLMESH.your_model_name`.
    *   **Development Environments (e.g., `my_dev`):** SQLMesh creates separate, isolated schemas for development environments. It usually does this by suffixing the production schema name with `__` and the environment name. For an environment named `my_dev`, look for a schema like `SQLMESH__MY_DEV` containing tables like `SQLMESH_DEMO_DB.SQLMESH__MY_DEV.your_model_name`.
4.  **Query Data:** Run `SELECT` statements against the tables in the appropriate schema to inspect the transformed data and verify the pipeline ran correctly.
    ```sql
    -- Example for production environment
    SELECT * FROM SQLMESH_DEMO_DB.SQLMESH.your_final_model LIMIT 10;

    -- Example for a development environment named 'my_dev'
    SELECT * FROM SQLMESH_DEMO_DB.SQLMESH__MY_DEV.your_final_model LIMIT 10;
    ```

### Comprehensive Cleanup

Ensure you remove *all* resources created:

1.  **Conveyor Resources:**
    ```bash
    conveyor project delete --name samples_sqlmesh_example --force
    ```
2.  **Snowflake Objects (SQLMesh - if run locally):** If you ran `uv run sqlmesh` commands locally, invalidate and clean the SQLMesh environments/schemas you created in your Snowflake account using [`sqlmesh invalidate`](https://sqlmesh.readthedocs.io/en/stable/reference/cli/#invalidate) and [`sqlmesh janitor`](https://sqlmesh.readthedocs.io/en/stable/reference/cli/#janitor).
    ```bash
    # Make sure your local config.yaml points to the correct Snowflake account
    uv run sqlmesh invalidate prod --sync
    uv run sqlmesh invalidate my_dev --sync # If you created dev environments
    uv run sqlmesh janitor --ignore-ttl
    ```
3.  **Snowflake Objects (Terraform - if applied):** If you ran `terraform apply` for local setup:
    ```bash
    cd infra
    terraform destroy 
    ```

### Conclusion

In this sample, we have seen how to develop and test a SQL-based data transformation pipeline locally using SQLMesh and `uv`, leveraging features like isolated [development environments](https://sqlmesh.readthedocs.io/en/stable/concepts/environments/) and [plans](https://sqlmesh.readthedocs.io/en/stable/concepts/plans/). Next, we learned how to integrate this SQLMesh project with Conveyor, defining an Airflow DAG to orchestrate the SQLMesh commands for planning and applying transformations in a managed environment. Last, we covered the basics of building (`conveyor build`), deploying (`conveyor deploy`), and running (`conveyor run task`) the SQLMesh project within a Conveyor environment.