
resource "snowflake_warehouse" "wh" {
  name = "COMPUTE_WH"
}

resource "snowflake_database" "db" {
  name = "DLT_DATA"
}

resource "snowflake_user" "user" {
  name     = var.snowflake_username
  password = var.snowflake_password
}

resource "snowflake_account_role" "dlt_loader" {
  name = "DLT_LOADER_ROLE"
}

resource "snowflake_grant_account_role" "grant_loader_role" {
  role_name = snowflake_account_role.dlt_loader.name
  user_name = snowflake_user.user.name
}

resource "snowflake_grant_privileges_to_account_role" "loader_use_db" {
  account_role_name = snowflake_account_role.dlt_loader.name
  privileges        = ["USAGE", "CREATE SCHEMA"]
  on_account_object {
    object_type = "DATABASE"
    object_name = snowflake_database.db.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "loader_use_wh" {
  account_role_name = snowflake_account_role.dlt_loader.name
  privileges        = ["USAGE"]
  on_account_object {
    object_type = "WAREHOUSE"
    object_name = snowflake_warehouse.wh.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "future_schema_grant_loader" {
  all_privileges    = true
  account_role_name = snowflake_account_role.dlt_loader.name
  on_schema {
    future_schemas_in_database = snowflake_database.db.name
  }
}


resource "snowflake_grant_privileges_to_account_role" "future_table_grant_loader" {
  all_privileges    = true
  account_role_name = snowflake_account_role.dlt_loader.name
  on_schema_object {
    future {
      object_type_plural = "TABLES"
      in_database        = snowflake_database.db.name
    }
  }
}
