terraform {
  required_version = "= 1.11.2"
  required_providers {
    conveyor = {
      source  = "datamindedbe/conveyor"
      version = "0.6.0"
    }
  }
}

provider "conveyor" {}
