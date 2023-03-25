import os
import boto3

def create_secret(secret_key, secret_value):
    sm = boto3.client('secretsmanager')

    response = sm.list_secrets()
    secrets =[ s['Name'] for s in response['SecretList'] ]

    if secret_key not in secrets:
        sm.create_secret(Name=secret_key, SecretString=secret_value)
        
totesys_password = os.environ['TOTESYS_PASSWORD']
totesys_username = os.environ['TOTESYS_USERNAME']
totesys_database_name = os.environ['TOTESYS_DATABASE_NAME'] 
totesys_host = os.environ['TOTESYS_HOST']
totesys_port = os.environ['TOTESYS_PORT']
totesys_region = os.environ['TOTESYS_REGION']

create_secret('TOTESYS_PASSWORD', totesys_password)
create_secret('TOTESYS_USERNAME', totesys_username)
create_secret('TOTESYS_DATABASE_NAME', totesys_database_name)
create_secret('TOTESYS_HOST', totesys_host)
create_secret('TOTESYS_PORT', totesys_port)
create_secret('TOTESYS_REGION', totesys_region)
