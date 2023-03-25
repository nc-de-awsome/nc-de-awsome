#!/bin/bash

cd ./venv/lib/python3.9/site-packages && pwd && zip -r ../deployment_requirements.zip .

cd ../../../.. && pwd

\cp  ./deploy_ingestion_lambda/lambda_handler.py ./dist/lambda_handler.py

cd ./dist && zip -r ../deployment_requirements.zip .