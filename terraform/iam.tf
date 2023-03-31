# --- INGEST LAMBDA ---
# Create a policy document for the ingestion lambda to access the relevant S3 resources
data "aws_iam_policy_document" "s3_document_ingest" {
  statement {
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.ingestion_zone.arn}/*"]
  }
}

# Create a policy document for the ingestion lambda to use CloudWatch
data "aws_iam_policy_document" "cw_document_ingest" {
  statement {
    actions   = ["logs:CreateLogGroup"]
    resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:*"]
  }
  statement {
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:log-group:/aws/lambda/${var.ingestion_lambda_name}:*"]
  }
}

# Create a policy document for the ingestion lambda to use Secrets Manager
data "aws_iam_policy_document" "sm_document_ingest" {
  statement {
    actions = ["secretsmanager:GetSecretValue"]
    resources = [
      "${data.aws_secretsmanager_secret.totesys_password.arn}",
      "${data.aws_secretsmanager_secret.totesys_username.arn}",
      "${data.aws_secretsmanager_secret.totesys_database_name.arn}",
      "${data.aws_secretsmanager_secret.totesys_host.arn}",
      "${data.aws_secretsmanager_secret.totesys_port.arn}",
      "${data.aws_secretsmanager_secret.totesys_region.arn}"
    ]
  }
}

# Create an S3 policy for the ingestion lambda
resource "aws_iam_policy" "s3_policy_ingest" {
  name_prefix = "s3-policy-${var.ingestion_lambda_name}-"
  policy      = data.aws_iam_policy_document.s3_document_ingest.json
}

# Create a CloudWatch policy for the ingestion lambda
resource "aws_iam_policy" "cw_policy_ingest" {
  name_prefix = "cw-policy-${var.ingestion_lambda_name}-"
  policy      = data.aws_iam_policy_document.cw_document_ingest.json
}

# Create a Secrets Manager policy for the ingestion lambda
resource "aws_iam_policy" "sm_policy_ingest" {
  name_prefix = "sm-policy-${var.ingestion_lambda_name}-"
  policy      = data.aws_iam_policy_document.sm_document_ingest.json
}

# Create an IAM role for the ingestion lambda
resource "aws_iam_role" "lambda_ingest_role" {
  name_prefix        = "role-${var.ingestion_lambda_name}-"
  assume_role_policy = <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": ["sts:AssumeRole"],
          "Principal": {
            "Service": ["lambda.amazonaws.com"]
          }
        }
      ]  
    }
  EOF
}

# Attach the S3, CW and SM policies to the IAM role
resource "aws_iam_role_policy_attachment" "s3_ingest_policy_attachment" {
  role       = aws_iam_role.lambda_ingest_role.name
  policy_arn = aws_iam_policy.s3_policy_ingest.arn
}

resource "aws_iam_role_policy_attachment" "cw_ingest_policy_attachment" {
  role       = aws_iam_role.lambda_ingest_role.name
  policy_arn = aws_iam_policy.cw_policy_ingest.arn
}

resource "aws_iam_role_policy_attachment" "sm_ingest_policy_attachment" {
  role       = aws_iam_role.lambda_ingest_role.name
  policy_arn = aws_iam_policy.sm_policy_ingest.arn
}

# --- PROCESS LAMBDA ---
# Create a policy document for the process lambda to access the relevant S3 resources
data "aws_iam_policy_document" "s3_document_process" {
  statement {
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.processed_zone.arn}/*"]
  }
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.ingestion_zone.arn}/*"]
  }
}

# Create a policy document for the process lambda to use CloudWatch
data "aws_iam_policy_document" "cw_document_process" {
  statement {
    actions   = ["logs:CreateLogGroup"]
    resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:*"]
  }
  statement {
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:log-group:/aws/lambda/${var.process_lambda_name}:*"]
  }
}

# Create an S3 policy for the process lambda
resource "aws_iam_policy" "s3_policy_process" {
  name_prefix = "s3-policy-${var.process_lambda_name}-"
  policy      = data.aws_iam_policy_document.s3_document_process.json
}

# Create a CloudWatch policy for the process lambda
resource "aws_iam_policy" "cw_policy_process" {
  name_prefix = "cw-policy-${var.process_lambda_name}-"
  policy      = data.aws_iam_policy_document.cw_document_process.json
}

# Create an IAM role for the process lambda
resource "aws_iam_role" "lambda_process_role" {
  name_prefix        = "role-${var.process_lambda_name}-"
  assume_role_policy = <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": ["sts:AssumeRole"],
          "Principal": {
            "Service": ["lambda.amazonaws.com"]
          }
        }
      ]  
    }
  EOF
}

# Attach the S3 and CW policies to the IAM role
resource "aws_iam_role_policy_attachment" "s3_process_policy_attachment" {
  role       = aws_iam_role.lambda_process_role.name
  policy_arn = aws_iam_policy.s3_policy_process.arn
}

resource "aws_iam_role_policy_attachment" "cw_process_policy_attachment" {
  role       = aws_iam_role.lambda_process_role.name
  policy_arn = aws_iam_policy.cw_policy_process.arn
}

# --- LOAD LAMBDA ---
# Create a policy document for the load lambda to access the relevant S3 resources
data "aws_iam_policy_document" "s3_document_load" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.processed_zone.arn}/*"]
  }
}

# Create a policy document for the load lambda to use CloudWatch
data "aws_iam_policy_document" "cw_document_load" {
  statement {
    actions   = ["logs:CreateLogGroup"]
    resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:*"]
  }
  statement {
    actions   = ["logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:log-group:/aws/lambda/${var.load_lambda_name}:*"]
  }
}

# Create a policy document for the load lambda to use Secrets Manager
data "aws_iam_policy_document" "sm_document_load" {
  statement {
    actions = ["secretsmanager:GetSecretValue"]
    resources = [
      "*"
    ]
  }
}

# Create an S3 policy for the load lambda
resource "aws_iam_policy" "s3_policy_load" {
  name_prefix = "s3-policy-${var.load_lambda_name}-"
  policy      = data.aws_iam_policy_document.s3_document_load.json
}

# Create a CloudWatch policy for the load lambda
resource "aws_iam_policy" "cw_policy_load" {
  name_prefix = "cw-policy-${var.load_lambda_name}-"
  policy      = data.aws_iam_policy_document.cw_document_load.json
}

# Create a Secrets Manager policy for the load lambda
resource "aws_iam_policy" "sm_policy_load" {
  name_prefix = "sm-policy-${var.load_lambda_name}-"
  policy      = data.aws_iam_policy_document.sm_document_load.json
}

# Create an IAM role for the load lambda
resource "aws_iam_role" "lambda_load_role" {
  name_prefix        = "role-${var.load_lambda_name}-"
  assume_role_policy = <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": ["sts:AssumeRole"],
          "Principal": {
            "Service": ["lambda.amazonaws.com"]
          }
        }
      ]  
    }
  EOF
}

# Attach the S3, CW and SM policies to the IAM role
resource "aws_iam_role_policy_attachment" "s3_load_policy_attachment" {
  role       = aws_iam_role.lambda_load_role.name
  policy_arn = aws_iam_policy.s3_policy_load.arn
}

resource "aws_iam_role_policy_attachment" "cw_load_policy_attachment" {
  role       = aws_iam_role.lambda_load_role.name
  policy_arn = aws_iam_policy.cw_policy_load.arn
}

resource "aws_iam_role_policy_attachment" "sm_load_policy_attachment" {
  role       = aws_iam_role.lambda_load_role.name
  policy_arn = aws_iam_policy.sm_policy_load.arn
}
