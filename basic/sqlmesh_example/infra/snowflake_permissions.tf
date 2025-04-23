resource "snowflake_user" "user" {
    name = "sqlmesh_demo_user"
    password = var.snowflake_password
}

resource "snowflake_warehouse" "wh" {
    name = "COMPUTE_WH"
}

resource "snowflake_database" "db" {
    name = "SQLMESH_DEMO_DB"
}

resource "snowflake_account_role" "sqlmesh" {
    name = "SQLMESH"
}

resource "snowflake_grant_privileges_to_account_role" "grant_wh_usage" {
    account_role_name = snowflake_account_role.sqlmesh.name
    privileges = ["USAGE"]
    on_account_object {
        object_type = "WAREHOUSE"
        object_name = snowflake_warehouse.wh.name
    }
}

resource "snowflake_grant_privileges_to_account_role" "grant_db_privilege" {
    account_role_name = snowflake_account_role.sqlmesh.name
    privileges = ["USAGE", "CREATE SCHEMA"]
    on_account_object {
        object_type = "DATABASE"
        object_name = snowflake_database.db.name
    }
}

resource "snowflake_grant_privileges_to_account_role" "future_schema_privilege" {
    privileges = ["USAGE", "CREATE TABLE", "CREATE VIEW"]
    account_role_name = snowflake_account_role.sqlmesh.name
    on_schema {
        future_schemas_in_database = snowflake_database.db.name
    }
}

resource "snowflake_grant_privileges_to_account_role" "future_table_privilege" {
    privileges = ["SELECT", "INSERT", "TRUNCATE", "UPDATE", "DELETE"]
    account_role_name = snowflake_account_role.sqlmesh.name
    on_schema_object {
        future {
            object_type_plural = "TABLES"
            in_database = snowflake_database.db.name
        }
    }
}

resource "snowflake_grant_privileges_to_account_role" "future_views_privilege" {
    privileges = ["REFERENCES", "SELECT"]
    account_role_name = snowflake_account_role.sqlmesh.name
    on_schema_object {
        future {
            object_type_plural = "VIEWS"
            in_database = snowflake_database.db.name
        }
    }
}

resource "snowflake_grant_account_role" "grant_sqlmesh_role" {
    role_name = snowflake_account_role.sqlmesh.name
    user_name = snowflake_user.user.name
}

resource "snowflake_grant_privileges_to_account_role" "grant_sample_db_privileges" {
    account_role_name = snowflake_account_role.sqlmesh.name
    privileges = ["IMPORTED PRIVILEGES"]
    on_account_object {
        object_type = "DATABASE"
        object_name = var.source_database
    }
}

resource "snowflake_grant_privileges_to_account_role" "grant_select_source_table" {
  privileges        = ["IMPORTED PRIVILEGES"]
  account_role_name = snowflake_account_role.sqlmesh.name
  on_schema_object {
    all {
      object_type_plural = "TABLES"
      in_database        = var.source_database
    }
  }
}
