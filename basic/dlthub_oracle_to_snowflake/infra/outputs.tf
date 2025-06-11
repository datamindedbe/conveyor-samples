output "rds_endpoint" {
  value = module.database.rds_endpoint
}

output snowflake_credentials {
    value = {
      host = "${lower(var.snowflake_organization_name)}-${var.snowflake_accountname}"
      warehouse = var.snowflake_warehouse
      database = module.snowflake-dlt-user.db
      username = var.snowflake_dlt_username
      password = var.snowflake_dlt_password
      role = module.snowflake-dlt-user.loader_role
    }
  sensitive = true
}