data "aws_caller_identity" "current_account" {}

data "aws_region" "current_region" {}

data "archive_file" "ingestion-lambda" {
    type = "zip"
    output_path = "${path.module}/../deploy_ingestion_lambda.zip"
    source_dir = "${path.module}/../deploy_ingestion_lambda"

    excludes    = [
    "__pycache__",
    "src/__pycache__",
    "tests/__pycache__",
    "tests",
    "src"
  ]

    depends_on = [null_resource.install_dependencies]
}

resource "null_resource" "install_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${path.module}/../requirements.txt -t ${path.module}/../deploy_ingestion_lambda/lib/python3.9/site-packages/ --upgrade"
  }
}

