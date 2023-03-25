#!/bin/bash
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

GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# echo "Enter commit message in or [x] to abort:"
# read msg2;

# if [ $msg2 != 'x' ]; then
#     git add . && git commit -m "$msg2" && git push origin $GIT_BRANCH
#     git checkout main
#     git merge $GIT_BRANCH
#     git checkout $GIT_BRANCH
# else
#     echo "Aborted"
# fi

fi