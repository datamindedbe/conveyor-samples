
variable "snowflake_password" {
  type      = string
  sensitive = true
}

variable "snowflake_username" {
  type      = string
  default = "loader"
  sensitive = false
}
