resource "aws_s3_bucket" "ingestion_zone" {
  bucket = "nc-de-awsome-ingestion-zone"
}

resource "aws_s3_bucket" "processed_zone" {
  bucket = "nc-de-awsome-processed-zone"
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "nc-de-awsome-code-bucket"
}

resource "aws_s3_object" "lambda_code_deployment" {
  bucket = aws_s3_bucket.lambda_bucket.bucket
  key    = "deploy_ingestion_lambda.zip"
  source = "${path.module}/../deployment_zips/deploy_ingestion_lambda.zip"
}
