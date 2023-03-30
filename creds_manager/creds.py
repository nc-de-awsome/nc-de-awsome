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

dw_password = os.environ['DW_PASSWORD']
dw_username = os.environ['DW_USERNAME']
dw_database_name = os.environ['DW_DATABASE_NAME'] 
dw_host = os.environ['DW_HOST']
dw_port = os.environ['DW_PORT']

create_secret('TOTESYS_PASSWORD', totesys_password)
create_secret('TOTESYS_USERNAME', totesys_username)
create_secret('TOTESYS_DATABASE_NAME', totesys_database_name)
create_secret('TOTESYS_HOST', totesys_host)
create_secret('TOTESYS_PORT', totesys_port)
create_secret('TOTESYS_REGION', totesys_region)

create_secret('DW_PASSWORD', dw_password)
create_secret('DW_USERNAME', dw_username)
create_secret('DW_DATABASE_NAME', dw_database_name)
create_secret('DW_HOST', dw_host)
create_secret('DW_PORT', dw_port)
