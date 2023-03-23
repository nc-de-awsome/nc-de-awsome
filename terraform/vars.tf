variable "ingestion_lambda_name" {
    type = string
    default = "ingestion-lambda"
}

variable "metric_namespace" {
    type = string
    default = "CustomMetrics"
}

variable "db_connection_error_metric_name" {
    type = string
    default = "DatabaseConnectionErrorCount"
}

variable "ingestion_error_metric_name" {
    type = string
    default = "IngestionErrorCount"
}

variable "write_error_metric_name" {
    type = string
    default = "WriteErrorCount"
}