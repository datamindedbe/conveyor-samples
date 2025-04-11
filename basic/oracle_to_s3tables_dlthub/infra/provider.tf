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
