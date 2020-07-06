locals {
  service_account_name = "openaq-dbt"
}

resource "kubernetes_service_account" "default" {
  metadata {
    name = local.service_account_name
    namespace = var.env_name
    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.default.arn
    }
  }
  automount_service_account_token = true
}
resource "aws_iam_role" "default" {
  name               = "openaq-dbt-${var.env_name}"
  path               = "/datafy-dp-${var.env_name}/"
  assume_role_policy = data.aws_iam_policy_document.default.json
}

data "aws_iam_policy_document" "default" {
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