
variable "snowflake_password" {
  type      = string
  description = "Password to be used by the snowflake user that will be given to dlthub as well."
  sensitive = true
}

variable "snowflake_username" {
  type      = string
  description = "Name of the user that will be given to dlthub as well."
  default = "loader"
}

variable "warehouse_name" {
  type      = string
  description = "Name of an existing Snowflake warehouse that dltHub may use"
  default = "loader"
}

variable "loader_role" {
  type = string
  description = "Name of the role that will be created and associated with the dlthub user."
  default = "DLT_LOADER_ROLE"
}