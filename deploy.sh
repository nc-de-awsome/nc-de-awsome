#!/bin/bash

# creates ingestion lambda deployment package zip
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

# creates process lambda deployment package zip
if [ -f ./deployment_zips/deploy_process_lambda.zip ]; then
    rm ./deployment_zips/deploy_process_lambda.zip
fi

mkdir -p deployment_zips/process_package

cp ./deploy_processed_lambda/main.py ./deployment_zips/process_package/main.py
pip install pandas --target deployment_zips/process_package/
pip install pyarrow --target deployment_zips/process_package/
pip install fastparquet --target deployment_zips/process_package/
pip install boto3 --target deployment_zips/process_package/
pip install pytz --target deployment_zips/process_package/
cd deployment_zips/process_package/
zip -r ../deploy_process_lambda.zip .
cd ..
cd ..
rm -r deployment_zips/process_package
