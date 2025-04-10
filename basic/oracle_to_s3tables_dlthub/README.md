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

   Oracle comes with its own demo schemas, like SH. We'll be using TPC-H though to allow benchmarking and have data of a certain size.
   Data is uploaded to _s3://tcph-100gb/_

   From there

3. Extract data using a dlt pipeline.


## Getting started

1. `uv sync` to create and populate the virtual environment containing the dependencies listed in the uv.lock file.
