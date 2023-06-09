variable "ingestion_lambda_name" {
  type    = string
  default = "ingestion-lambda"
}

variable "process_lambda_name" {
  type    = string
  default = "process-lambda"
}

variable "load_lambda_name" {
  type    = string
  default = "load-lambda"
}

variable "metric_namespace" {
  type    = string
  default = "CustomMetrics"
}

variable "ingestion_error_metric_name" {
  type    = string
  default = "IngestionErrorCount"
}

variable "transformation_error_metric_name" {
  type    = string
  default = "TransformationErrorCount"
}

variable "load_error_metric_name" {
  type    = string
  default = "LoadErrorCount"
}
