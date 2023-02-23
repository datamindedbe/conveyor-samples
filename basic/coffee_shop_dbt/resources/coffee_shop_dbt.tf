locals {
  project_name = "coffee_shop_dbt"
  uuid_pattern = "????????-????-????-????-????????????"
}

resource "aws_iam_role" "default" {
  name               = "${local.project_name}-${var.env_name}"
  assume_role_policy = data.aws_iam_policy_document.default_assume_role.json
}

data "aws_iam_policy_document" "default_assume_role" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringLike"
      variable = "${replace(var.aws_iam_openid_connect_provider_url, "https://", "")}:sub"
      values   = ["system:serviceaccount:${var.env_name}:${replace(local.project_name, "_", ".")}-${local.uuid_pattern}"]
    }

    principals {
      identifiers = [var.aws_iam_openid_connect_provider_arn]
      type        = "Federated"
    }
  }
}

resource "aws_iam_role_policy" "s3_permissions" {
  name   = "s3_permissions"
  role   = aws_iam_role.default.id
  policy = data.aws_iam_policy_document.s3_permissions.json
}

data "aws_iam_policy_document" "s3_permissions" {
  statement {
    actions = [
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::datafy-demo-data",
      "arn:aws:s3:::datafy-demo-data/*",
    ]
    effect = "Allow"
  }
}