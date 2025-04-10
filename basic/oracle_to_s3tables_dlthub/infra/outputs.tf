output "rds_endpoint" {
  value = aws_db_instance.rds.endpoint
}

output "rds_port" {
  value = aws_db_instance.rds.port
}

output "rds_id" {
  value = aws_db_instance.rds.id
}

output "rds_instance_class" {
  value = aws_db_instance.rds.instance_class
}

output "rds_engine" {
  value = aws_db_instance.rds.engine
}

output "rds_username" {
  value = aws_db_instance.rds.username
}

output "rds_db_name" {
  value = aws_db_instance.rds.db_name
}

output "rds_allocated_storage" {
  value = aws_db_instance.rds.allocated_storage
}

output "rds_storage_type" {
  value = aws_db_instance.rds.storage_type
}

output "rds_engine_version" {
  value = aws_db_instance.rds.engine_version
}

output "rds_deletion_protection" {
  value = aws_db_instance.rds.deletion_protection
}

output "rds_multi_az" {
  value = aws_db_instance.rds.multi_az
}

output "rds_backup_retention_period" {
  value = aws_db_instance.rds.backup_retention_period
}

output "rds_backup_window" {
  value = aws_db_instance.rds.backup_window
}

output "rds_maintenance_window" {
  value = aws_db_instance.rds.maintenance_window
}

output "rds_parameter_group_name" {
  value = aws_db_instance.rds.parameter_group_name
}

output "rds_option_group_name" {
  value = aws_db_instance.rds.option_group_name
}

output "rds_subnet_group_name" {
  value = aws_db_instance.rds.db_subnet_group_name
}

output "rds_security_group_ids" {
  value = aws_db_instance.rds.vpc_security_group_ids
}

output "rds_kms_key_id" {
  value = aws_db_instance.rds.kms_key_id
}

output "security_group_name" {
  value = aws_security_group.test_security_group.name
}

output "policy_arn" {
  value = aws_iam_policy.policy.arn
}
output "role_arn" {
  value = aws_iam_role.integration.arn
}