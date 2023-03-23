resource "aws_sns_topic" "error_alerts" {
    name = "error-alerts-topic"
}

resource "aws_sns_topic_subscription" "error_alerts_target" {
    topic_arn = aws_sns_topic.error_alerts.arn
    protocol = "email"
    endpoint = "nc.de.awsome@gmail.com"
}