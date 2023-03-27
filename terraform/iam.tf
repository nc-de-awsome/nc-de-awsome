data "aws_iam_policy_document" "s3_document_ingest" {
  statement {
      actions = ["s3:PutObject"]
      resources = [
        "${aws_s3_bucket.ingestion_zone.arn}/*"
      ]
  }
  
  statement {
    actions = ["secretsmanager:GetSecretValue"]
    resources = [
      "*" # replace with ARN of the AWS secrets location
    ]
  }
}

data "aws_iam_policy_document" "cw_document" {
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

resource "aws_iam_policy" "s3_policy_ingest" {
  name_prefix = "s3-policy-${var.ingestion_lambda_name}"
  policy      = data.aws_iam_policy_document.s3_document_ingest.json
}

resource "aws_iam_policy" "cw_policy" {
  name_prefix = "cw-policy"
  policy      = data.aws_iam_policy_document.cw_document.json
}


resource "aws_iam_role" "lambda_ingest_role" {
  name_prefix        = "role-${var.ingestion_lambda_name}"
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

resource "aws_iam_role_policy_attachment" "s3_ingest_policy_attachment" {
  role       = aws_iam_role.lambda_ingest_role.name
  policy_arn = aws_iam_policy.s3_policy_ingest.arn
}

resource "aws_iam_role_policy_attachment" "cw_ingest_policy_attachment" {
  role       = aws_iam_role.lambda_ingest_role.name
  policy_arn = aws_iam_policy.cw_policy.arn
}

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

resource "aws_iam_role" "lambda_process_role" {
  name_prefix        = "role-${var.process_lambda_name}"
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

resource "aws_iam_policy" "s3_policy_process" {
  name_prefix = "s3-policy-${var.process_lambda_name}"
  policy      = data.aws_iam_policy_document.s3_document_process.json
}

resource "aws_iam_role_policy_attachment" "s3_process_policy_attachment" {
  role       = aws_iam_role.lambda_process_role.name
  policy_arn = aws_iam_policy.s3_policy_process.arn
}

# data "aws_iam_policy_document" "cw_document" {
#     statement {
#         actions = ["logs:CreateLogGroup"]
#         resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:*"]
#         }
#     statement {
#         actions = ["Logs:CreateLogStream",
#                     "logs:PutLogEvents"]
#         resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:log-group:/aws/lambda/${var.process_lambda_name}:*"]
#         }
# }

# resource "aws_iam_role_policy_attachment" "cw_process_policy_attachment" {
#     role = aws_iam_role.lambda_process_role.name
#     policy_arn = aws_iam_policy.cw_policy.arn
# }




