To set up a connection between the dlt-app and Snowflake, see this on the dlt docs.

Next, you'll likely want to create a read-only role on the tables in that schema, and grant yourself access to that role, so that you can verify what dlt did. See [snowflake.sql](./snowflake.sql)
