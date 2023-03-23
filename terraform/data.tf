data "aws_caller_identity" "current_account" {}

data "aws_region" "current_region" {}

data "archive_file" "ingestion-lambda" {
    type = "zip"
    output_path = "${path.module}/../ingestion-function.zip"
    source_dir = "${path.module}/../src"
}