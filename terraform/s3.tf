resource "aws_s3_bucket" "ingestion_zone" {
    bucket_prefix = "ingestion-zone-"
}

resource "aws_s3_bucket" "processed_zone" {
    bucket_prefix = "processed-zone-"
}