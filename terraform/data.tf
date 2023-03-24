data "aws_caller_identity" "current_account" {}

data "aws_region" "current_region" {}

data "archive_file" "ingestion-lambda" {
    type = "zip"
    output_path = "${path.module}/../deploy_ingestion_lambda.zip"
    source_dir = "${path.module}/../deploy_ingestion_lambda"
    excludes = "${path.module}/../deployment_ingestion_lambda/test.zip"
}