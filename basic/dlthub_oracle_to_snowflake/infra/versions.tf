terraform {
  required_version = ">= 0.13"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.94.1"
    }
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "1.0.5"
    }
  }

  backend "s3" {
    bucket       = "" # manually created (the bootstrap problem), with versioning enabled (best practice)
    key          = ""
    region       = ""
    use_lockfile = ""
  }
}