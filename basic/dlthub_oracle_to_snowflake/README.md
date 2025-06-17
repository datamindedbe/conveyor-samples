# Oracle to Snowflake using dltHub

This project illustrates how one can extract data from an Oracle database and
load those into a Snowflake data warehouse using [dltHub][dlt]. Conveyor is used
to facilitate scheduling and deployment.

An Oracle database will be provisioned on an existing AWS account. Data (from
the TPC-H benchmark) will be loaded into it, using an S3 bucket as an
intermediary. The actual dltHub pipelines will copy this data from Oracle into a
Snowflake account you have access to as well.

## Prerequisites

You have

- an AWS account in which
  - you can create secrets in the Secrets Manager
  - you have created an S3 bucket for the purpose of this Conveyor sample
  - you can create an RDS instance
- a Snowflake account with an existing warehouse you have access to and have
  privileges to
  - create a user
  - create a database
  - create a role,
  - and grant privileges to the role
- Docker installed locally
- Conveyor installed locally

### Quickstart

💡 To save time, steps 1 and 2, can and should be executed in parallel.

1. Generate and upload [TPC-H][tpch] data to an AWS S3 bucket you have write
   access to.

   Modify the environment variables used in
   [./scripts/gen_data.sh](./scripts/gen_data.sh) as needed:

   ```sh
   BUCKET=tpc-h-sets PREFIX=1GB SCALE_FACTOR=1 ./scripts/gen_data.sh
   ```

2. Provision the RDS for Oracle db instance and a write-enabled login for dltHub
   on your existing Snowflake account.

   Change at a minimum the bucket in
   [infra/aws_s3.tfbackend](infra/aws_s3.tfbackend), which states where
   Terraform will hold your remote state. Then:

   ```sh
   terraform -chdir=infra init -backend-config=aws_s3.tfbackend
   ```

   Next, apply the actual configuration:

   ```sh
   terraform -chdir=infra apply
   ```

   Fill in the prompts with values of your choosing.

3. Populate the Oracle instance with the data you've uploaded in step 1:

   1. Obtain the RDS endpoint (aka HOST):

      ```sh
      terraform -chdir=infra output rds_endpoint
      ```

   2. Obtain Oracle credentials:

      ```sh
      secret=$(aws secretsmanager list-secrets \
        --filters \
          Key=owning-service,Values=rds \
          Key=tag-key,Values=Project \
          Key=tag-value,Values=DltConveyorSample \
        --query 'SecretList[].Name' \
        --output text)

      aws secretsmanager get-secret-value \
        --secret-id "${secret}" \
        --query SecretString \
      | jq '. | fromjson'
      ```

   3. Initiate the data transfer from S3 to Oracle.

      Start by modifying the `p_bucket_name` and `p_s3_prefix` in
      [./scripts/transfer_data.sql](./scripts/transfer_data.sql) to the values
      you supplied in step 1 of this list. Then, adjust the placeholders USER,
      PASS and HOST with the output from the first 2 steps in this list of the
      following command and execute it:

      ```sh
      docker run \
        --volume ./scripts:/data:ro \
        --rm \
        oracletools/sqlplus:v19.18_lin \
          "${USER}/${PASS}@${HOST}/ORCL" \
          @/data/transfer_data.sql
      ```

   4. Wait until the data transfer is complete (adjust the placeholders USER,
      PASS and HOST with the output from the first 2 steps in this list, and
      adjust the task-number with the output from the previous command):

      ```sh
      TASKNUMBER=1234567-89

      docker run  \
        --rm \
        --interactive \
        oracletools/sqlplus:v19.18_lin \
          "${USER}/${PASS}@${HOST}/ORCL" <<EOF
          SELECT text FROM table(
              rdsadmin.rds_file_util.read_text_file(
                  'BDUMP',
                  'dbtask-${TASKNUMBER}.log'
              )
          );
        EOF
      ```

      If you see something like:

      ```text
      [INFO ] The task finished successfully.
      ```

      then the task is complete and you can continue with the next step.

      More details about this log file and how to read it, can be found on the
      [AWS documentation for transferring files from S3 to Amazon RDS for
      Oracle][s3toOracle].

   5. Load the data and create the dltHub read-only user (adjust the
      placeholders USER, PASS and HOST with the output from the first 2 steps in
      this list):

      ```sh
      docker run \
      --volume ./scripts:/data:ro \
      --rm \
      oracletools/sqlplus:v19.18_lin \
        -S \
        "${USER}/${PASS}@${HOST}/ORCL" \
        @/data/load_data_add_users.sql
      ```

       Note: the SQL script is based on [a blog post by Sean D.
       Stuber][tuber-blog] and changed only in small ways.

   6. Initialize this folder as a project: `conveyor project create --name
      dlthub`
   7. Build the project: `conveyor build`
   8. Deploy the project to the samples environment: `conveyor deploy --env
      samples --wait`
   9. *(Add any specific commands needed to trigger or observe the sample, e.g.,
      `conveyor run task <task_name>`, instructions to check output in
      S3/database)* @TODO complete
   10. Cleanup:

       ```sh
       conveyor project delete --name dlthub --force
       terraform -chdir=infra destroy
       ```

### Walkthrough

1. The *quickstart* sets you up with a dataset about 1GB in size spread over
   multiple tables in a single schema, `tpch`.

   - You can modify the size of the tables generated by TPC-H's dbgen utility:
     simply change the `SCALE_FACTOR`.

   For the [Hashicorp Terraform][tf] parts, if you don't want to type the
   variables that you'll be prompted for, when invoking actions like `terraform
   apply`, add them to a file called `terraform.tfvars`, or `user.auto.tfvars`,
   which will be [ignored by Git](./infra/.gitignore) to prevent it from
   accidentally getting committed to your code repo. Terraform [automatically
   loads such a file][auto.tfvars], if it has that exact name. As an example,
   the following would be great to fill in and use for your `terraform.tfvars`:

   ```text
   # Identify your Snowflake account
   snowflake_accountname = "..."
   snowflake_organization_name = "..."
   snowflake_username = "..."
   snowflake_role = "..."  # A role the above user can assume and with which 
                           # a database and a user can be created.
   
   # Credentials for the dlthub user on Snowflake
   snowflake_dlt_username = "..."
   snowflake_dlt_password = "..."
   
   # Resources that the dlthub user will use on Snowflake
   snowflake_warehouse = "..."
   
   # Details for setting up the Oracle instance
   aws_account = "..."
   db_subnets = ["...", "..."]
   vpc_id = "..."
   ```

### 🚀 Using dltHub

We use [`uv`](https://github.com/astral-sh/uv) to manage Python dependencies
efficiently. Here's how to get started:

#### 🔧 Setup

1. [Install `uv`](https://github.com/astral-sh/uv?tab=readme-ov-file#installation)
2. **Install this project's dependencies:**

   This will automatically create a virtual environment as well.

   ```bash
   uv sync
   ```

   You might need some non-Python software as well, like clang. Install those
   using your operating system's tooling.

#### ▶️ Running Pipelines

To run a specific pipeline script, execute

```bash
uv run <pipeline_file>.py
```

---

#### 📊 Viewing Tables

To inspect the available tables in a pipeline:

```bash
dlt pipeline <pipeline_name> show
```

The `pipeline_name`s are given in [.dlt/config.toml](.dlt/config.toml).

## Cleanup

When you're done experimenting with the sample, run `terraform destroy` from the
*infra* folder. This will clean up all the resources that were provisioned.

[dlt]: https://dlthub.com/
[tpch]: https://www.tpc.org/tpch/
[tf]: https://developer.hashicorp.com/terraform
[auto.tfvars]: https://developer.hashicorp.com/terraform/language/values/variables#variable-definitions-tfvars-files
[s3toOracle]: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/oracle-s3-integration.using.html#oracle-s3-integration.using.task-status
[tuber-blog]: https://seanstuber.com/2017/05/27/setting-up-tpc-h-test-data-with-oracle-on-linux/
