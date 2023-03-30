resource "aws_cloudwatch_log_group" "ingestion_zone_log" {
    name = "/aws/lambda/${var.ingestion_lambda_name}"
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
    alarm_description         = "This metric checks for any issue with the ingestion lambda"
    alarm_actions             = ["${aws_sns_topic.error_alerts.arn}"]
}

resource "aws_cloudwatch_log_group" "process_zone_log" {
    name = "/aws/lambda/${var.process_lambda_name}"
}

resource "aws_cloudwatch_log_metric_filter" "transformation_error" {
    name = "TransformationErrorFilter"
    pattern = "TransformationError"
    log_group_name = aws_cloudwatch_log_group.process_zone_log.name

    metric_transformation {
        name      = var.transformation_error_metric_name
        namespace = var.metric_namespace
        value     = "1"
    }
}

resource "aws_cloudwatch_metric_alarm" "alert_transformation_error" {
    alarm_name                = "TransformationErrorAlarm"
    comparison_operator       = "GreaterThanOrEqualToThreshold"
    evaluation_periods        = "1"
    metric_name               = var.transformation_error_metric_name
    namespace                 = var.metric_namespace
    period                    = "60"
    statistic                 = "Sum"
    threshold                 = "1"
    actions_enabled           = "true"
    alarm_description         = "This metric checks for any issue with the process lambda"
    alarm_actions             = ["${aws_sns_topic.error_alerts.arn}"]
}