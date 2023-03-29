# --- INGEST LAMBDA ---

# creates policy document for ingestion lambda to access relevant s3 resources
data "aws_iam_policy_document" "s3_document_ingest" {
  statement {
      actions = ["s3:PutObject"]
      resources = [
        "${aws_s3_bucket.ingestion_zone.arn}/*"
      ]
  }
}

# creates policy document for ingest lambda to use CloudWatch log groups
data "aws_iam_policy_document" "cw_document_ingest" {
  statement {
    actions   = ["logs:CreateLogGroup"]
    resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:*"]
  }
  statement {
    actions = ["Logs:CreateLogStream",
    "logs:PutLogEvents"]
    resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:log-group:/aws/lambda/${var.ingestion_lambda_name}:*"]
  }
}

# creates policy document for ingest lambda to use Secrets Manager
data "aws_iam_policy_document" "sm_document_ingest" {
  statement {
    actions = ["secretsmanager:GetSecretValue"]
    resources = [
      "${data.aws_secrets_manager_secret.totesys_password.arn}",
      "${data.aws_secrets_manager_secret.totesys_username.arn}",
      "${data.aws_secrets_manager_secret.totesys_database_name.arn}",
      "${data.aws_secrets_manager_secret.totesys_host.arn}",
      "${data.aws_secrets_manager_secret.totesys_port.arn}",
      "${data.aws_secrets_manager_secret.totesys_region.arn}"
    ]
  }
}

# creates s3 policy for ingest lambda
resource "aws_iam_policy" "s3_policy_ingest" {
  name_prefix = "s3-policy-${var.ingestion_lambda_name}-"
  policy      = data.aws_iam_policy_document.s3_document_ingest.json
}

# creates CloudWatch policy for ingest lambda
resource "aws_iam_policy" "cw_policy_ingest" {
  name_prefix = "cw-policy-${var.ingestion_lambda_name}-"
  policy      = data.aws_iam_policy_document.cw_document_ingest.json
}

# creates Secrets Manager policy for ingest lambda
resource "aws_iam_policy" "sm_policy_ingest" {
  name_prefix = "sm-policy-${var.ingestion_lambda_name}-"
  policy      = data.aws_iam_policy_document.sm_document_ingest.json
}


# creates ingest lambda role
resource "aws_iam_role" "lambda_ingest_role" {
  name_prefix        = "role-${var.ingestion_lambda_name}-"
  assume_role_policy = <<EOF
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole"
            ],
            "Principal": {
                "Service": [
                    "lambda.amazonaws.com"
                ]
            }
        }
    ]  
}
EOF
}

# attach ingest lambda policies to ingest lambda role
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

# creates policy document for process lambda to access relevant s3 resources
data "aws_iam_policy_document" "s3_document_process" {
  statement {
    actions = ["s3:PutObject"]
    resources = [
      "${aws_s3_bucket.processed_zone.arn}/*"
    ]
  }
  statement {
    actions = ["s3:GetObject"]
    resources = [
      "${aws_s3_bucket.ingestion_zone.arn}/*"
    ]
  }
}

# creates policy document for process lambda to use CloudWatch log groups
data "aws_iam_policy_document" "cw_document_process" {
    statement {
        actions = ["logs:CreateLogGroup"]
        resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:*"]
        }
    statement {
        actions = ["Logs:CreateLogStream",
                    "logs:PutLogEvents"]
        resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:log-group:/aws/lambda/${var.process_lambda_name}:*"]
        }
}
# creates s3 policy for process lambda
resource "aws_iam_policy" "s3_policy_process" {
  name_prefix = "s3-policy-${var.process_lambda_name}-"
  policy      = data.aws_iam_policy_document.s3_document_process.json
}

# creates CloudWatch policy for process lambda
resource "aws_iam_policy" "cw_policy_process" {
  name_prefix = "cw-policy-${var.process_lambda_name}-"
  policy      = data.aws_iam_policy_document.cw_document_process.json
}

# creates ingest lambda role
resource "aws_iam_role" "lambda_process_role" {
  name_prefix        = "role-${var.process_lambda_name}-"
  assume_role_policy = <<EOF
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole"
            ],
            "Principal": {
                "Service": [
                    "lambda.amazonaws.com"
                ]
            }
        }
    ]  
}
EOF
}

# attach process lambda policies to process lambda role
resource "aws_iam_role_policy_attachment" "s3_process_policy_attachment" {
  role       = aws_iam_role.lambda_process_role.name
  policy_arn = aws_iam_policy.s3_policy_process.arn
}

resource "aws_iam_role_policy_attachment" "cw_process_policy_attachment" {
    role = aws_iam_role.lambda_process_role.name
    policy_arn = aws_iam_policy.cw_policy_process.arn
}