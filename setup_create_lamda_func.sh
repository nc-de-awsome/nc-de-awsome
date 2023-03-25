#!/bin/bash

mkdir -p dist/ingest_package
cp  ./deploy_ingestion_lambda/lambda_handler.py ./dist/lambda_handler.py

# rm ./dist/deployment_requirements.zip
pip install pg8000 --target dist/ingest_package
pip install boto3 --target dist/ingest_package
cd dist/ingest_package
zip -r ../deployment_requirements.zip .
cd ..
zip deployment_requirements.zip lambda_handler.py
rm -r ingest_package
cd ..

# _____

# cd ./venv/lib/python3.9/site-packages && pwd && zip -r ../deployment_requirements.zip .

# cd ../../../.. && pwd

# \cp  ./deploy_ingestion_lambda/lambda_handler.py ./dist/lambda_handler.py

# cd ./dist && zip -r ../deployment_requirements.zip .

# # _____


# rm src/ingest_deployment.zip
# pip install psycopg2-binary --target src/ingest_package
# pip install datetime --target src/ingest_package
# cd src/ingest_package
# zip -r ../ingest_deployment.zip .
# cd ..
# zip ingest_deployment.zip ingest_data.py
# rm -r ingest_package
# cd ..