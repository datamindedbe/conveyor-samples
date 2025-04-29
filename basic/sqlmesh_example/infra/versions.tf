terraform {
  required_version = ">= 0.13"
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "1.0.5"
    }
  }

  backend "s3" {
    bucket       = "terraform-states-dm" # manually created (the bootstrap problem), with versioning enabled (best practice)
    key          = "sqlmesh-demo"
    region       = "eu-west-1"
    # use_lockfile = true
  }
}