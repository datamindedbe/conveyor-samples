locals {
  region  = "eu-west-1"
  bucket  = "tcph-100gb"
  account = "299641483789" # dm-playground
}

resource "aws_db_instance" "rds" {
  identifier                            = var.db_identifier
  engine                                = var.db_engine
  engine_version                        = var.db_engine_version
  allocated_storage                     = var.db_allocated_storage
  license_model                         = var.db_license_model
  instance_class                        = var.db_instance_class
  port                                  = var.db_port
  username                              = var.username
  manage_master_user_password           = var.manage_master_user_password
  character_set_name                    = var.db_character_set_name
  availability_zone                     = data.aws_availability_zones.available_zones.names[0]
  db_subnet_group_name                  = aws_db_subnet_group.database_subnet_group.name
  parameter_group_name                  = var.db_param_group
  option_group_name                     = aws_db_option_group.s3connection.name
  storage_type                          = var.db_storage_type
  copy_tags_to_snapshot                 = var.copy_tags_to_snapshot
  backup_retention_period               = var.db_backup_retention
  backup_window                         = var.db_backup_window
  maintenance_window                    = var.db_maintenance_window
  multi_az                              = var.db_multi_az
  kms_key_id                            = var.kms_key_id
  apply_immediately                     = var.db_apply_mods_immediate
  auto_minor_version_upgrade            = var.db_minor_upgrades
  allow_major_version_upgrade           = var.db_major_upgrades
  snapshot_identifier                   = var.db_snapshot
  vpc_security_group_ids                = [aws_security_group.test_security_group.id]
  skip_final_snapshot                   = var.skip_final_snapshot
  monitoring_interval                   = var.monitoring_interval
  monitoring_role_arn                   = var.monitoring_role_arn
  performance_insights_enabled          = var.performance_insights_enabled
  performance_insights_retention_period = var.performance_insights_retention_period
  deletion_protection                   = var.deletion_protection
  max_allocated_storage                 = var.max_allocated_storage
  tags                                  = var.tags
  delete_automated_backups              = var.delete_automated_backups
  publicly_accessible                   = var.publically_accessible
}


resource "aws_db_option_group" "s3connection" {
  name                     = "load-from-s3"
  option_group_description = "Allow Oracle to read from an S3 bucket"
  engine_name              = var.db_engine
  major_engine_version     = split(".", var.db_engine_version)[0]

  option {
    option_name = "S3_INTEGRATION"
    version     = "1.0"
  }
}

resource "aws_iam_policy" "policy" {
  name        = "rds-s3-integration"
  path        = "/"
  description = "Enable Oracle for RDS to read from an S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:PutObject",
          "s3:*"
        ]
        Effect = "Allow"
        Resource = [
          "arn:aws:s3:::${local.bucket}",
          "arn:aws:s3:::${local.bucket}/*",
        ]
      },
    ]
  })
}

resource "aws_iam_role" "integration" {
  name = "rds-s3-integration"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect : "Allow"
        Principal = {
          Service = "rds.amazonaws.com"
        }
        Condition = {
          StringEquals = {
            "aws:SourceAccount" : "${local.account}",
            "aws:SourceArn" : "arn:aws:rds:${local.region}:${local.account}:db:${aws_db_instance.rds.identifier}"
          }
        }
      }
    ]
  })
}

# Note: you must attach this role to the RDS instance still

resource "aws_iam_role_policy_attachment" "integration" {
  policy_arn = aws_iam_policy.policy.arn
  role       = aws_iam_role.integration.name
}
