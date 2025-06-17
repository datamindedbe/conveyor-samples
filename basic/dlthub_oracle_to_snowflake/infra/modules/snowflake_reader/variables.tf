variable "snowflake_password" {
  type      = string
  sensitive = true
}

variable "snowflake_username" {
  type      = string
  default = "loader"
  sensitive = false
}

variable "role_name" {
  type      = string
  description = "Name of the read-only role to be created"
  default = "DLT_READER_ROLE"
}

variable "db_name" {
  type      = string
  description = "Name of the database to which to grant _usage_ rights."
  # snowflake_database.db.name
}

variable "warehouse_name" {
  type      = string
  description = "Name of the warehouse to which to grant _usage_ rights."
  # snowflake_database.db.name
}

variable users {
  type = set
  description = "list of the Snowflake users you want to grand read privileges to"
}
