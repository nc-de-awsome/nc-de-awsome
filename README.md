# AWSome group project

## Introduction
This project creates a data platform in AWS (using S3, Lambda, EventBridge and CloudWatch) that extracts data from an operational database (named totesys), archives it in a data lake, and makes it available in a remodelled OLAP data warehouse.

A Python application deployed in AWS Lambda (hereafter named ingestion lambda) ingests all tables from the totesys database and saves them in an S3 bucket (ingestion zone bucket). It runs automatically every 10 minutes according to an Eventbridge rule and logs progress to CloudWatch. Email alerts are triggered in the event of errors.

## Platform Infrastructure
The data platform has two s3 buckets: an ingestion zone bucket; and a processed zone bucket.

The following AWS sources have permission to access each Lambda function as follows:
    - EventBridge rule to invoke ingestion lambda every 10 minutes
    - [S3 ingestion-zone bucket/EventBridge rule] to invoke transformation lambda

The ingestion lambda has permission to:
    - create S3 objects in the ingestion zone bucket
    - create CloudWatch logs

The transformation lambda has permission to:
    - read S3 objects in the ingestion zone bucket
    - create S3 objects in the processed zone bucket
    - create CloudWatch logs

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

