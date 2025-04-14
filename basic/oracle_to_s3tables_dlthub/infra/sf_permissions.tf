locals {
  dm_users = toset(["SIYAN_LUO", "OLIVER_WILLEKENS"])
}

resource "snowflake_warehouse" "wh" {
  name = "COMPUTE_WH"
}

resource "snowflake_database" "db" {
  name = "dlt_data"
}

resource "snowflake_user" "user" {
  name     = "loader"
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

resource "snowflake_account_role" "dlt_reader" {
  name = "DLT_READER_ROLE"
}

resource "snowflake_grant_account_role" "grant_reader_role" {
  for_each  = local.dm_users
  role_name = snowflake_account_role.dlt_reader.name
  user_name = each.key
}

resource "snowflake_grant_privileges_to_account_role" "reader_use_db" {
  account_role_name = snowflake_account_role.dlt_reader.name
  privileges        = ["USAGE"]
  on_account_object {
    object_type = "DATABASE"
    object_name = snowflake_database.db.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "reader_use_wh" {
  account_role_name = snowflake_account_role.dlt_reader.name
  privileges        = ["USAGE"]
  on_account_object {
    object_type = "WAREHOUSE"
    object_name = snowflake_warehouse.wh.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "all_schemas_grant" {
  all_privileges    = true
  account_role_name = snowflake_account_role.dlt_reader.name
  on_schema {
    all_schemas_in_database = snowflake_database.db.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "select_table_grant" {
  privileges        = ["SELECT"]
  account_role_name = snowflake_account_role.dlt_reader.name
  on_schema_object {
    all {
      object_type_plural = "TABLES"
      in_database        = snowflake_database.db.name
    }
  }
}

resource "snowflake_grant_privileges_to_account_role" "future_schema_grant_reader" {
  all_privileges    = true
  account_role_name = snowflake_account_role.dlt_reader.name
  on_schema {
    future_schemas_in_database = snowflake_database.db.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "future_table_grant_reader" {
  privileges        = ["SELECT"]
  account_role_name = snowflake_account_role.dlt_reader.name
  on_schema_object {
    future {
      object_type_plural = "TABLES"
      in_database        = snowflake_database.db.name
    }
  }
}

variable "snowflake_password" {
  type      = string
  sensitive = true
}


variable "loaded_schema" {
  type      = string
  sensitive = false
  default   = "SH_FULL"
}