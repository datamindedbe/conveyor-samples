terraform {
  required_version = ">= 0.13"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.94.1"
    }
  }

  backend "s3" {
    bucket       = "terraform-states-dm" # manually created (the bootstrap problem), with versioning enabled (best practice)
    key          = "dlthub-demo"
    region       = "eu-west-1"
    use_lockfile = true
  }

}
