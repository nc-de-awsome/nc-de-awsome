# AWSome group project

## Introduction
This project creates a data platform in AWS (using S3, Lambda, EventBridge, Secrets Manager and CloudWatch) that extracts data from an operational database (named totesys), archives it in a data lake, and makes it available in a remodelled OLAP data warehouse.

A Python application deployed in AWS Lambda (hereafter named ingest lambda) ingests all tables from the totesys database and stores them in an S3 bucket (ingestion zone bucket). It runs on a schedule every 10 minutes according to an Eventbridge rule and logs progress to CloudWatch. Email alerts are triggered in the event of errors.

A second Python application (hereafter named process lambda) uses the ingested tables to populate dimension and fact tables of 3 star schemas. It saves these remodelled tables in parquet format in a separate S3 bucket (processed zone bucket). The process lambda is automatically triggered when the ingest lambda creates a file on completion named query_log.json in the ingestion zone bucket. Progress is logged to CloudWatch. Email alerts are triggered in the event of errors.

A final third Python application (hereafter named load lambda) loads the processed data into a prepared data warehouse. It is automatically trigged when the process lambda creates a file on completion named query_log.json in the processed zone bucket. Progress is logged to CloudWatch. Email alerts are triggered in the event of errors.

## Platform Infrastructure
The data platform has two s3 buckets: an ingestion zone bucket; and a processed zone bucket.

The following AWS sources have permission to access each Lambda function as follows:
    - EventBridge rule (named every_ten_minutes) - allowed to invoke ingest lambda
    - S3 ingestion zone bucket - allowed to invoke process lambda 
    - S3 processed zone bucket - allowed to invoke load lambda

The ingest lambda has permission to:
    - create CloudWatch logs (aws/lambda/ingestion-lambda)
    - create S3 objects in the ingestion zone bucket
    - read specific secrets in Secrets Manager

The process lambda has permission to:
    - create CloudWatch logs (aws/lambda/process-lambda)
    - read S3 objects in the ingestion zone bucket
    - create S3 objects in the processed zone bucket

The load lambda has permission to:
    - create CloudWatch logs (aws/lambda/load-lambda)
    - read S3 objects in the processed zone bucket
    - read specific secrests in Secrets Manager

## Instructions for setup

1. Fork and clone this project.
2. In the terminal, navigate to the root directory of the project, and run:

   ```bash
   sh setup.sh
   ```

   This creates venv and installs project requirements.

3. Following this, in the terminal, navigate to the root directory of the project, and run:

   ```bash
   sh state.sh
   ```

   This creates an s3 bucket that will store the terraform state file remotely.

4. Deployment of AWS resources are automated using GitHub Actions.

