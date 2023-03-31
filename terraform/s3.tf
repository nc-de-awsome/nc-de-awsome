resource "aws_s3_bucket" "ingestion_zone" {
  bucket = "nc-de-awsome-ingestion-zone"
}

resource "aws_s3_bucket" "processed_zone" {
  bucket = "nc-de-awsome-processed-zone"
}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "nc-de-awsome-code-bucket"
}

resource "aws_s3_object" "ingest_lambda_code_deployment" {
  bucket = aws_s3_bucket.lambda_bucket.bucket
  key    = "deploy_ingestion_lambda.zip"
  source = "${path.module}/../deployment_zips/deploy_ingestion_lambda.zip"
}

resource "aws_s3_object" "process_lambda_code_deployment" {
  bucket = aws_s3_bucket.lambda_bucket.bucket
  key    = "deploy_process_lambda.zip"
  source = "${path.module}/../deployment_zips/deploy_process_lambda.zip"
}

# resource "aws_s3_object" "load_lambda_code_deployment" {
#   bucket = aws_s3_bucket.lambda_bucket.bucket
#   key    = "deploy_load_lambda.zip"
#   source = "${path.module}/../deployment_zips/deploy_load_lambda.zip"
# }

resource "aws_s3_bucket_notification" "ingest_bucket_notification" {
  bucket = aws_s3_bucket.ingestion_zone.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.process_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "query_log"
    filter_suffix       = ".json"
  }

  depends_on = [aws_lambda_permission.allow_s3_ingestion_zone_bucket]
}

# resource "aws_s3_bucket_notification" "load_bucket_notification" {
#   bucket = aws_s3_bucket.processed_zone.id

#   lambda_function {
#     lambda_function_arn = aws_lambda_function.load_lambda.arn
#     events              = ["s3:ObjectCreated:*"]
#     filter_prefix       = "query_log"
#     filter_suffix       = ".json"
#   }

#   depends_on = [aws_lambda_permission.allow_s3_processed_zone_bucket]
# }