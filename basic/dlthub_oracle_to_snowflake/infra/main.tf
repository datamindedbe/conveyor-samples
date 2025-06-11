module "database" {
  source = "./modules/terraform-aws-rds-oracle"

  aws_account = var.aws_account
  aws_region = var.aws_region
  db_subnet_ids    = var.db_subnets
  vpc_id       = var.vpc_id
  db_engine_version = "19.0.0.0.ru-2022-10.rur-2022-10.r1"
  db_allocated_storage = 400
  db_instance_class = "db.t3.small"
  db_port = "11555"  # Changed from default 1521 to something a little harder to find by attackers
  s3_bucket = "tpc-h-sets"
}

module snowflake-dlt-user {
  source = "./modules/snowflake_loader"

  snowflake_password = var.snowflake_dlt_password
  snowflake_username = var.snowflake_dlt_username
  warehouse_name = var.snowflake_warehouse
}