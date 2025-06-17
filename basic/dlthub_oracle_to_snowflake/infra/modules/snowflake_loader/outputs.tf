output db {
  value = snowflake_database.db.name
}

output loader_role {
  value = lower(snowflake_account_role.dlt_loader.name)
}