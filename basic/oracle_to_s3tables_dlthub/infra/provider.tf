provider "aws" {
  region = "eu-west-1"

  default_tags {
    tags = {
      Author           = "Oliver"
      Project          = "DltConveyorSample"
      ExpectedLifetime = "2025Q2"
    }
  }
}

provider "snowflake" {
  role              = "ACCOUNTADMIN"
  organization_name = "iqorzws"
  account_name      = "playground"
  authenticator     = "ExternalBrowser"
  user              = var.snowflake_username
}
