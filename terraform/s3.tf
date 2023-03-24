resource "aws_s3_bucket" "ingestion_zone" {
    bucket = "nc-de-awsome-ingestion-zone"
}

resource "aws_s3_bucket" "processed_zone" {
    bucket = "nc-de-awsome-processed-zone"
}

resource "aws_s3_object_copy" "lambda_code_deployment" {
  bucket = "nc-de-awsome-state"
  key    = "deployment_requirements.zip"
  source = "${path.module}/../deployment_requirements.zip"
}

data "aws_s3_bucket_object" "lambda_code_deployment" {
    bucket = "nc-de-awsome-state"
    key = "deployment_requirements.zip"
}