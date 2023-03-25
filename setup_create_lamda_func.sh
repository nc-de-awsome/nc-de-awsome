#!/bin/bash

\cp  ./deploy_ingestion_lambda/lambda_handler.py ./dist/lambda_handler.py

cd ./dist && zip -r ../deployment_requirements.zip .