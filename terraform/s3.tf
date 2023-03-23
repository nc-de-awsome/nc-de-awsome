resource "aws_s3_bucket" "ingestion_zone" {
    bucket = "nc-de-awsome-ingestion-zone"
}

resource "aws_s3_bucket" "processed_zone" {
    bucket = "nc-de-awsome-processed-zone"
}