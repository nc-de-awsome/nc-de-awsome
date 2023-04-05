resource "aws_lambda_function" "ingest_lambda" {
  s3_bucket        = aws_s3_bucket.lambda_bucket.bucket
  s3_key           = aws_s3_object.ingest_lambda_code_deployment.key
  function_name    = var.ingestion_lambda_name
  role             = aws_iam_role.lambda_ingest_role.arn
  handler          = "lambda_handler.ingest"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("${path.module}/../deployment_zips/deploy_ingestion_lambda.zip")
  timeout          = 60
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_ingest_lambda" {
  statement_id  = "AllowIngestLambdaExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ingest_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_ten_minutes.arn
}

# handler and source_code_hash to be updated as needed
resource "aws_lambda_function" "process_lambda" {
  s3_bucket        = aws_s3_bucket.lambda_bucket.bucket
  s3_key           = aws_s3_object.process_lambda_code_deployment.key
  function_name    = var.process_lambda_name
  role             = aws_iam_role.lambda_process_role.arn
  handler          = "lambda_handler.transform"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("${path.module}/../deployment_zips/deploy_process_lambda.zip")
  timeout          = 120
}

resource "aws_lambda_permission" "allow_s3_ingestion_zone_bucket" {
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.process_lambda.function_name
  principal      = "s3.amazonaws.com"
  source_arn     = aws_s3_bucket.ingestion_zone.arn
  source_account = data.aws_caller_identity.current_account.account_id
}

# handler and source_code_hash to be updated as needed
resource "aws_lambda_function" "load_lambda" {
  s3_bucket        = aws_s3_bucket.lambda_bucket.bucket
  s3_key           = aws_s3_object.load_lambda_code_deployment.key
  function_name    = var.load_lambda_name
  role             = aws_iam_role.lambda_load_role.arn
  handler          = "lambda_handler.load"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("${path.module}/../deployment_zips/deploy_load_lambda.zip")
  timeout          = 900
}

resource "aws_lambda_permission" "allow_s3_processed_zone_bucket" {
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.load_lambda.function_name
  principal      = "s3.amazonaws.com"
  source_arn     = aws_s3_bucket.processed_zone.arn
  source_account = data.aws_caller_identity.current_account.account_id
}
