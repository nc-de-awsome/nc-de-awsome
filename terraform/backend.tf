terraform{
    backend "s3" {
        bucket = "nc-de-awsome-state"
        key = "terraform.tfstate"
        region = "eu-west-2"
    }
}