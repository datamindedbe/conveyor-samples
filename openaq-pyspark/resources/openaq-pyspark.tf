resource "aws_iam_role" "openaq-pyspark" {
  name               = "openaq-pyspark-${var.env_name}"
  path               = "/datafy-dp-${var.env_name}/"
  assume_role_policy = data.aws_iam_policy_document.openaq-pyspark-assume-role.json
}

data "aws_iam_policy_document" "openaq-pyspark-assume-role" {
  statement {
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      type        = "AWS"
      identifiers = [var.env_worker_role]
    }
    effect = "Allow"
  }
}

resource "aws_iam_role_policy" "openaq-pyspark" {
  name   = "openaq-pyspark"
  role   = aws_iam_role.openaq-pyspark.id
  policy = data.aws_iam_policy_document.openaq-pyspark.json
}

data "aws_iam_policy_document" "openaq-pyspark" {
  statement {
    actions = [
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::openaq-fetches",
      "arn:aws:s3:::openaq-fetches/*",
      "arn:aws:s3:::datafy-training",
      "arn:aws:s3:::datafy-training/*"
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