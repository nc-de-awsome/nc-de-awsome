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
# to update handler and source_code_hash as needed
resource "aws_lambda_function" "process_lambda" {
  s3_bucket        = aws_s3_bucket.lambda_bucket.bucket
  s3_key           = aws_s3_object.process_lambda_code_deployment.key
  function_name    = var.process_lambda_name
  role             = aws_iam_role.lambda_process_role.arn
  handler          = "main.transform"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("${path.module}/../deployment_zips/deploy_process_lambda.zip")
  timeout          = 60
}

# draft code for process lambda permission to trigger (source_arn tbc)
# resource "aws_lambda_permission" "allow_cloudwatch_to_call_process_lambda" {
#   statement_id  = "AllowProcessLambdaExecutionFromCloudWatch"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.process_lambda.function_name
#   principal     = "events.amazonaws.com"
#   source_arn    = aws_cloudwatch_event_rule.every_ten_minutes.arn
# }
