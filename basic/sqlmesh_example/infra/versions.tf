terraform {
  required_version = ">= 0.13"
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "1.0.5"
    }
  }
}