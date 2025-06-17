terraform {
  required_version = ">= 0.13"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.94.1"
    }
    snowflake = {
      source  = "snowflakedb/snowflake"
      version = "2.1.0"
    }
  }

  backend "s3" {
    bucket       = "" # manually created (the bootstrap problem), with versioning enabled (best practice)
    key          = ""
    region       = ""
    use_lockfile = ""
  }
}

provider "aws" {
  region = "eu-west-1"

  default_tags {
    tags = {
      Project          = "DltConveyorSample"
    }
  }
}

provider "snowflake" {
  organization_name = var.snowflake_organization_name
  account_name      = var.snowflake_accountname
  user              = var.snowflake_username
  role              = var.snowflake_role  # Should have sufficient privileges
  authenticator     = "ExternalBrowser"
}
