resource "aws_s3_bucket" "ingestion_zone" {
    bucket = "nc-de-awsome-ingestion-zone"
}

resource "aws_s3_bucket" "processed_zone" {
    bucket = "nc-de-awsome-processed-zone"
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "nc-de-awsome-code-bucket"
}

resource "aws_s3_object_copy" "lambda_code_deployment" {
  bucket = aws_s3_bucket.lambda_bucket.bucket
  key    = "deployment_requirements.zip"
  source = "${path.module}/../deployment_requirements.zip"
}
