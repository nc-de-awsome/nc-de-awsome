terraform{
    backend "s3" {
        bucket = "nc-de-awsome-state"
        key = "project/terraform.tfstate"
        region = "us-east-1"
    }
}