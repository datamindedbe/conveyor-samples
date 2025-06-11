variable "tags" {
  type = any
  default = {
    source   = "conveyor-sample"
    purpose = "experiment with dlthub and oracle as an ingestion source"
  }
}

variable "snowflake_role" {
  description = "The Snowflake role with which to create a user for dltHub to create relations."
  type = string
}

variable "snowflake_organization_name" {
  description = "Name of the organization the Snowflake account belongs to."
  type = string
}

variable "snowflake_accountname" {
  description = "The name of the Snowflake account in which data will be transferred."
  type = string
}

variable "snowflake_username" {
  description = "The name of the user with which to authenticate against Snowflake to create resources."
  type = string
}

variable "snowflake_dlt_username" {
  description = "The name of the Snowflake user that dltHub will use."
  type = string
}

variable "snowflake_dlt_password" {
  description = "The password of the Snowflake user that dltHub will use"
  type = string
}

variable "snowflake_warehouse" {
  description = "Name of the warehouse that the dlthub loader role may use."
  type = string
}

variable "aws_account" {
  description = "AWS Account id in which the resources should be provisioned."
  type = string
}

variable "aws_region" {
  description = "AWS Region in which the resources should be provisioned."
  type = string
  default = "eu-west-1"
}


variable "vpc_id" {
  description = "Id of the VPC in which to launch the RDS database"
}

variable "db_subnets" {
  description = "Subnets in which to launch the database"
}
