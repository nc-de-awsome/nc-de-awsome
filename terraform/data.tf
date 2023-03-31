data "aws_caller_identity" "current_account" {}

data "aws_region" "current_region" {}

data "aws_secretsmanager_secret" "totesys_password" {
  name = "TOTESYS_PASSWORD"
}

data "aws_secretsmanager_secret" "totesys_username" {
  name = "TOTESYS_USERNAME"
}

data "aws_secretsmanager_secret" "totesys_database_name" {
  name = "TOTESYS_DATABASE_NAME"
}

data "aws_secretsmanager_secret" "totesys_host" {
  name = "TOTESYS_HOST"
}

data "aws_secretsmanager_secret" "totesys_port" {
  name = "TOTESYS_PORT"
}

data "aws_secretsmanager_secret" "totesys_region" {
  name = "TOTESYS_REGION"
}

# data "aws_secretsmanager_secret" "dw_password" {
#   name = "DW_PASSWORD"
# }

# data "aws_secretsmanager_secret" "dw_username" {
#   name = "DW_USERNAME"
# }

# data "aws_secretsmanager_secret" "dw_database_name" {
#   name = "DW_DATABASE_NAME"
# }

# data "aws_secretsmanager_secret" "dw_host" {
#   name = "DW_HOST"
# }

# data "aws_secretsmanager_secret" "dw_port" {
#   name = "DW_PORT"
# }

