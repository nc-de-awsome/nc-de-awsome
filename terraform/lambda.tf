resource "aws_lambda_function" "ingest_lambda" {
    # filename = "${path.module}/../deployment_requirements.zip"
    filename = data.aws_s3_bucket_object.lambda_code_deployment.id
    function_name = var.ingestion_lambda_name
    role = aws_iam_role.lambda_ingest_role.arn
    handler = "deployment_requirements.lambda_handler.ingest"
    runtime = "python3.9"
    source_code_hash = data.archive_file.ingestion-lambda.output_base64sha256
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_ingest_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.ingest_lambda.function_name 
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.every_ten_minutes.arn
}