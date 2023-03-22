resource "aws_cloudwatch_event_rule" "every_ten_minutes" {
    name = "every-ten-minutes"
    description = "Fires every ten minutes"
    schedule_expression = "rate(10 minutes)"
}

resource "aws_cloudwatch_event_target" "run_lambda_every_ten_minutes" {
    rule = aws_cloudwatch_event_rule.every_ten_minutes.name
    target_id = "run_lambda"
    arn = aws_lambda_function.check_foo.arn # the arn of the Lambda 'ingestion' function
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_ingest_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.check_foo.function_name # the name of the Lambda 'ingestion' function
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.every_ten_minutes.arn
}