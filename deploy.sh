#!/bin/bash

if [ -f ./dist/deploy_ingestion_lambda.zip ]; then
    rm ./dist/deploy_ingestion_lambda.zip
fi

mkdir -p dist/ingest_package

cp ./deploy_ingestion_lambda/lambda_handler.py ./dist/ingest_package/lambda_handler.py
pip install pg8000 --target dist/ingest_package/
pip install boto3 --target dist/ingest_package/

cd dist/ingest_package/
zip -r ../deploy_ingestion_lambda.zip .
cd ..
cd ..
rm -r dist/ingest_package