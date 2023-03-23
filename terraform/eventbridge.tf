resource "aws_cloudwatch_event_rule" "every_ten_minutes" {
    name = "every-ten-minutes"
    description = "Fires every ten minutes"
    schedule_expression = "rate(10 minutes)"
}

resource "aws_cloudwatch_event_target" "run_lambda_every_ten_minutes" {
    rule = aws_cloudwatch_event_rule.every_ten_minutes.name
    target_id = "run_lambda"
    arn = aws_lambda_function.ingest_lambda.arn 
}

