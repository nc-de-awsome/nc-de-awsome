#!/bin/bash

loop=true
while loop==true
echo "Ready to deploy? [y/n]"
read input
do
    if [ $input == 'n' ] || [ $input == 'y' ]; then
        loop=false
        break
    fi
    echo "Invalid input"
done

if [ $input == 'n' ]; then
    echo "Aborted"
else

LAMBDA_FILE="lambda_handler.py"
LAMBDA_HANDLER_PATH="./deploy_ingestion_lambda/$LAMBDA_FILE"
ZIP_FILE="deployment_requirements.zip"
ZIP_PATH="./dist/$ZIP_FILE"
INGEST_PACKAGE="dist/ingest_package"

mkdir -p $INGEST_PACKAGE
cp $LAMBDA_HANDLER_PATH ./dist/$LAMBDA_FILE

if [ -f $ZIP_PATH ]; then
    rm $ZIP_PATH
fi

pip install pg8000 --target $INGEST_PACKAGE
pip install boto3 --target $INGEST_PACKAGE
zip -r dist/$ZIP_FILE $INGEST_PACKAGE
zip dist/$ZIP_FILE dist/$LAMBDA_FILE
rm -r $INGEST_PACKAGE
rm dist/$LAMBDA_FILE

GIT_BRANCH="git rev-parse --abbrev-ref HEAD)"

echo "Enter commit message:"
read msg
while [ -n $msg ]
do
    echo "Enter commit message or [x] to abort:"
    read msg
    if [ $msg == 'x' ]; then
        echo "Aborting"
        return
    fi
done
echo ${GIT_BRANCH}

git add . && git commit -m "$msg" && git push origin $GIT_BRANCH

fi