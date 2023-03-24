import os
import boto3

def create_secret(secret_key, secret_value):
    sm = boto3.client('secretsmanager')
    sm.create_secret(Name=secret_key, SecretString=secret_value, ForceOverwriteReplicaSecret=True)

totesys_password = os.environ['TOTESYS_PASSWORD']
totesys_username = os.environ['TOTESYS_USERNAME']
totesys_database_name = os.environ['TOTESYS_DATABASE_NAME'] 
totesys_host = os.environ['TOTESYS_HOST']
totesys_port = os.environ['TOTESYS_PORT']
totesys_region = os.environ['TOTESYS_REGION']

create_secret('TOTESYS_PASSWORD', totesys_password)
create_secret('TOTESYS_USERNAME', totesys_username)
create_secret('TOTESYS_DATABASE_NAME', totesys_username)
create_secret('TOTESYS_HOST', totesys_username)
create_secret('TOTESYS_PORT', totesys_username)
create_secret('TOTESYS_REGION', totesys_username)