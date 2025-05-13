provider "aws" {
  region = "eu-west-1"

  default_tags {
    tags = {
      Project          = "DltConveyorSample"
    }
  }
}

provider "snowflake" {
  role              = var.snowflake_role  # Should have sufficient privileges
  organization_name = var.snowflake_organization_name
  account_name      = var.snowflake_accountname
  authenticator     = "ExternalBrowser"
  user              = var.snowflake_username
}
