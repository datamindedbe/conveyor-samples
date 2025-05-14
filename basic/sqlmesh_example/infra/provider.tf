provider "snowflake" {
  role              = "ACCOUNTADMIN"
  organization_name = var.organization_name
  account_name      = var.account_name
  authenticator     = "ExternalBrowser"
  user              = var.snowflake_username
}