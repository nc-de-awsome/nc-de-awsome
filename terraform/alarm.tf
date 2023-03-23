resource "aws_cloudwatch_log_group" "ingestion_zone_log"{
    name = "/aws/lambda/${var.ingestion_lambda_name}"
}

resource "aws_cloudwatch_log_metric_filter" "db_connection_error" {
    name = "DatabaseConnectionErrorFilter"
    pattern = "DatabaseConnectionError"
    log_group_name = aws_cloudwatch_log_group.ingestion_zone_log.name

    metric_transformation {
        name      = var.db_connection_error_metric_name
        namespace = var.metric_namespace
        value     = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_db_connection_error" {
    alarm_name                = "DatabaseConnectionErrorAlarm"
    comparison_operator       = "GreaterThanOrEqualToThreshold"
    evaluation_periods        = "1"
    metric_name               = var.db_connection_error_metric_name
    namespace                 = var.metric_namespace
    period                    = "60"
    statistic                 = "Sum"
    threshold                 = "1"
    actions_enabled           = "true"
    alarm_description         = "This metric checks for any issue with connecting to the database"
    alarm_actions             = ["${aws_sns_topic.error_alerts.arn}"]
}

resource "aws_cloudwatch_log_metric_filter" "ingestion_error" {
    name = "IngestionErrorFilter"
    pattern = "IngestionError"
    log_group_name = aws_cloudwatch_log_group.ingestion_zone_log.name

    metric_transformation {
        name      = var.ingestion_error_metric_name
        namespace = var.metric_namespace
        value     = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_ingestion_error" {
    alarm_name                = "IngestionErrorAlarm"
    comparison_operator       = "GreaterThanOrEqualToThreshold"
    evaluation_periods        = "1"
    metric_name               = var.ingestion_error_metric_name
    namespace                 = var.metric_namespace
    period                    = "60"
    statistic                 = "Sum"
    threshold                 = "1"
    actions_enabled           = "true"
    alarm_description         = "This metric checks for any fail query to the database by the ingestion lambda"
    alarm_actions             = ["${aws_sns_topic.error_alerts.arn}"]
}

resource "aws_cloudwatch_log_metric_filter" "write_error" {
    name = "WriteErrorFilter"
    pattern = "WriteError"
    log_group_name = aws_cloudwatch_log_group.ingestion_zone_log.name

    metric_transformation {
        name      = var.write_error_metric_name
        namespace = var.metric_namespace
        value     = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_write_error" {
    alarm_name                = "WriteErrorAlarm"
    comparison_operator       = "GreaterThanOrEqualToThreshold"
    evaluation_periods        = "1"
    metric_name               = var.write_error_metric_name
    namespace                 = var.metric_namespace
    period                    = "60"
    statistic                 = "Sum"
    threshold                 = "1"
    actions_enabled           = "true"
    alarm_description         = "This metric checks for any issue with writing JSON to the S3 ingestion bucket"
    alarm_actions             = ["${aws_sns_topic.error_alerts.arn}"]
}