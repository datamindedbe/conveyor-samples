variable "organization_name" {
    type = string
    description = "The organization name for the snowflake account"
    sensitive = false
}   

variable "account_name" {
    type = string
    description = "The name of the snowflake account"
    sensitive = false
}

variable "snowflake_username" {
    type = string
    description = "Please input your DM email address for login the playgroud account"
    sensitive = false
}

variable "snowflake_password" {
    type = string
    description = "The password for the service user - sqlmesh_demo_user"
    sensitive = true
}

variable "source_database" {
    type = string
    description = "The source database, this is required to grant access to the database"
    sensitive = false
    default = "SNOWFLAKE_SAMPLE_DATA"
}

variable "warehouse" {
    type = string
    sensitive = false
    default = "COMPUTE_WH"
}