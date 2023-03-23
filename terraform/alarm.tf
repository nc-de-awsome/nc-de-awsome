resource "aws_cloudwatch_log_group" "ingestion_zone_log"{
    name = "/aws/lambda/${var.ingestion_lambda_name}"
}

resource "aws_cloudwatch_log_metric_filter" "ingestion_db_connection_error" {
    name = "DatabaseConnectionErrorFilter"
    pattern = "DatabaseConnectionError"
    log_group_name = aws_cloudwatch_log_group.ingestion_zone_log.name

    metric_transformation {
        name      = var.ingestion_db_connection_error_metric_name
        namespace = var.metric_namespace
        value     = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_ingestion_db_connection_error" {
    alarm_name                = "DatabaseConnectionErrorAlarm"
    comparison_operator       = "GreaterThanOrEqualToThreshold"
    evaluation_periods        = "1"
    metric_name               = var.ingestion_db_connection_error_metric_name
    namespace                 = var.metric_namespace
    period                    = "60"
    statistic                 = "Sum"
    threshold                 = "1"
    alarm_description         = "This metric checks for any inability to connect to the database."
    alarm_actions             = ["arn:aws:sns:us-east-1:341652476000:test-error-alerts"]
}

