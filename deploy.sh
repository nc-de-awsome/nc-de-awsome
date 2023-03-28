#!/bin/bash

if [ -f ./deployment_zips/deploy_ingestion_lambda.zip ]; then
    rm ./deployment_zips/deploy_ingestion_lambda.zip
fi

mkdir -p deployment_zips/ingest_package

cp ./deploy_ingestion_lambda/lambda_handler.py ./deployment_zips/ingest_package/lambda_handler.py
pip install pg8000 --target deployment_zips/ingest_package/
pip install boto3 --target deployment_zips/ingest_package/
pip install pytz --target deployment_zips/ingest_package/

cd deployment_zips/ingest_package/
zip -r ../deploy_ingestion_lambda.zip .
cd ..
cd ..
rm -r deployment_zips/ingest_package
