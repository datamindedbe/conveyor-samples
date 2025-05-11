resource "snowflake_account_role" "this" {
  name = var.role_name
}

resource "snowflake_grant_account_role" "grant_reader_role" {
  for_each  = var.users
  role_name = snowflake_account_role.this.name
  user_name = each.key
}

resource "snowflake_grant_privileges_to_account_role" "use_db" {
  account_role_name = snowflake_account_role.this.name
  privileges        = ["USAGE"]
  on_account_object {
    object_type = "DATABASE"
    object_name = var.db_name
  }
}

resource "snowflake_grant_privileges_to_account_role" "use_wh" {
  account_role_name = snowflake_account_role.this.name
  privileges        = ["USAGE"]
  on_account_object {
    object_type = "WAREHOUSE"
    object_name = var.warehouse_name
  }
}

resource "snowflake_grant_privileges_to_account_role" "use_all_schemas" {
  all_privileges    = true
  account_role_name = snowflake_account_role.this.name
  on_schema {
    all_schemas_in_database = var.db_name
  }
}

resource "snowflake_grant_privileges_to_account_role" "select_table_grant" {
  privileges        = ["SELECT"]
  account_role_name = snowflake_account_role.this.name
  on_schema_object {
    all {
      object_type_plural = "TABLES"
      in_database        = var.db_name
    }
  }
}

resource "snowflake_grant_privileges_to_account_role" "future_schema_grant_reader" {
  all_privileges    = true
  account_role_name = snowflake_account_role.this.name
  on_schema {
    future_schemas_in_database = var.db_name
  }
}

resource "snowflake_grant_privileges_to_account_role" "future_table_grant_reader" {
  privileges        = ["SELECT"]
  account_role_name = snowflake_account_role.this.name
  on_schema_object {
    future {
      object_type_plural = "TABLES"
      in_database        = var.db_name
    }
  }
}
