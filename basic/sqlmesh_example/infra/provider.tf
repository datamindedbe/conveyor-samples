provider "snowflake" {
  role              = "ACCOUNTADMIN"
  organization_name = "iqorzws"
  account_name      = "playground"
  authenticator     = "ExternalBrowser"
  user              = var.snowflake_username
}