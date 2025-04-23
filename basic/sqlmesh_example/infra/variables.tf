variable "snowflake_username" {
    type = string
    sensitive = false
}

variable "snowflake_password" {
    type = string
    sensitive = true
}

variable "source_database" {
    type = string
    sensitive = false
}

variable "warehouse" {
    type = string
    sensitive = false
}