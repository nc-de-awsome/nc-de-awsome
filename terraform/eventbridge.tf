resource "aws_cloudwatch_event_rule" "every_ten_minutes" {
  name                = "every-ten-minutes"
  description         = "Fires every ten minutes"
  schedule_expression = "rate(10 minutes)"
}

resource "aws_cloudwatch_event_target" "run_ingestion_lambda_every_ten_minutes" {
  rule      = aws_cloudwatch_event_rule.every_ten_minutes.name
  target_id = "run_ingestion_lambda"
  arn       = aws_lambda_function.ingest_lambda.arn
}

# UNUSED CODE
# resource "aws_cloudwatch_event_rule" "ingestion_log_created" {
#   name                = "ingestion-log-created"
#   description         = "Fires once the query_log has been created on ingest completion"
#   event_pattern       = <<EOF
#     {
#       "source": ["aws.s3"],
#       "detail-type": ["Object Created"],
#       "resources": ["${aws_s3_bucket.ingestion_zone.arn}"],
#       "detail": {
#         "bucket": {
#           "name": ["${aws_s3_bucket.ingestion_zone.id}"]
#         },
#         "object": {
#           "key": ["query_log.json"]
#         },
#         "reason": ["PutObject"]
#       }
#     }
#   EOF
# }

# resource "aws_cloudwatch_event_target" "run_process_lambda_on_ingest_completion" {
#   rule      = aws_cloudwatch_event_rule.ingestion_log_created.name
#   target_id = "run_process_lambda"
#   arn       = aws_lambda_function.process_lambda.arn
# }