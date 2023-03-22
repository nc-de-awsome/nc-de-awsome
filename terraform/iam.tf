data "aws_iam_policy_document" "s3_document_ingest" {
    statement {
        actions = ["s3:PutObject"]
        resources = [
            "${aws_s3_bucket.ingestion_zone.arn}/*"
            ]
        }
    #add another statement depending on what ingestion access needed in s3    
}
data "aws_iam_policy_document" "cw_document" {
    statement {
        actions = ["logs:CreateLogGroup"]
        resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:*"]
        }
    statement {
        actions = ["Logs:CreateLogStream",
                    "logs:PutLogEvents"]
        resources = ["arn:aws:logs:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:log-group:/aws/lambda/demo_lambda:*"]
        }
}
resource "aws_iam_policy" "s3_policy_ingest" {
    name_prefix = "s3-ingest-policy"
    policy = data.aws_iam_policy_document.s3_document_ingest.json
}
resource "aws_iam_policy" "cw_policy" {
    name_prefix = "cw-policy"
    policy = data.aws_iam_policy_document.cw_document.json
}

resource "aws_iam_role" "lambda_ingest_role" {
    name_prefix = "role-ingest-lambda"
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
    role = aws_iam_role.lambda_ingest_role.name
    policy_arn = aws_iam_policy.s3_policy_ingest.arn
}
resource "aws_iam_role_policy_attachment" "cw_ingest_policy_attachment" {
    role = aws_iam_role.lambda_ingest_role.name
    policy_arn = aws_iam_policy.cw_policy.arn
}
# data "aws_iam_policy_document" "eventbridge_document" {
#     statement {
#         actions = ["events:EnableRule"]
#         resources = [xxxxx arn from evenbridge rule]
#         }
# }
# resource "aws_iam_policy" "eventbridge_policy" {
#     name_prefix = "eventbridge-policy"
#     policy = data.aws_iam_policy_document.eventbridge_document.json
# }
# resource "aws_iam_role_policy_attachment" "eventbridge_policy_attachment" {
#     role = aws_iam_role.lambda_ingest_role.name
#     policy_arn = aws_iam_policy.eventbridge_policy.arn
# }


# DRAFT CODE FOR RDS PERMISSION(ADD TO IAM ROLE)**
#"Statement": [
#         {
#             "Effect": "Allow",
#             "Action": [
#                 "rds-db:connect"
#             ],
#             "Resource": [
#                 "arn:aws:rds-db:${data.aws_region.current_region.name}:${data.aws_caller_identity.current_account.account_id}:dbuser:
#             ]
#         }
#     ]
