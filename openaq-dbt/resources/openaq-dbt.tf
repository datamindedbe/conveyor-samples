locals {
  service_account_name = "openaq-dbt"
}

resource "kubernetes_service_account" "default" {
  metadata {
    name = local.service_account_name
    namespace = var.env_name
    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.openaq-dbt.arn
    }
  }
  automount_service_account_token = true
}
resource "aws_iam_role" "openaq-dbt" {
  name               = "openaq-dbt-${var.env_name}"
  path               = "/datafy-dp-${var.env_name}/"
  assume_role_policy = data.aws_iam_policy_document.openaq-dbt-assume-role.json
}

resource "aws_iam_role_policy" "openaq-dbt" {
  name   = "openaq-dbt"
  role   = aws_iam_role.openaq-dbt.id
  policy = data.aws_iam_policy_document.openaq-dbt.json
}

data "aws_iam_policy_document" "openaq-dbt-assume-role" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      variable = "${replace(var.aws_iam_openid_connect_provider_url, "https://", "")}:sub"
      values   = ["system:serviceaccount:${var.env_name}:${local.service_account_name}"]
    }

    principals {
      identifiers = [var.aws_iam_openid_connect_provider_arn]
      type        = "Federated"
    }
  }
}

data "aws_iam_policy_document" "openaq-dbt" {
  statement {
    actions = [
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::datafy-training",
      "arn:aws:s3:::datafy-training/*"
    ]
    effect = "Allow"
  }

  statement {
    actions = [
      "athena:*"
    ]
    resources = [
      "arn:aws:athena:eu-west-1:130966031144:*"
    ]
    effect = "Allow"
  }

  statement {
    actions = [
      "glue:GetDatabase"
    ]
    resources = [
      "*"
    ]
    effect = "Allow"
  }

  statement {
    actions = [
      "glue:*"
    ]
    resources = [
      "arn:aws:glue:${var.aws_region}:${var.aws_account_id}:catalog",
      "arn:aws:glue:${var.aws_region}:${var.aws_account_id}:database/datafy_glue",
      "arn:aws:glue:${var.aws_region}:${var.aws_account_id}:table/datafy_glue/*"
    ]
    effect = "Allow"
  }
}