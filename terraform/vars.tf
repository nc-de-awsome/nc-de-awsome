variable "ingestion_lambda_name" {
    type = string
    default = "xxxxxxxxxxxxxx" # to be replaced with lambda ingestion function.
}

variable "metric_namespace" {
    type = string
    default = "CustomMetrics"
}

variable "ingestion_db_connection_error_metric_name" {
    type = string
    default = "DatabaseConnectionErrorCount"
}