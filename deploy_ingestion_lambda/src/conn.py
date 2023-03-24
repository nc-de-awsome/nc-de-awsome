# '''
#     conn.py contains utility functions which load the required credentials to access the Totesys database from GitHub secrets
# '''
# import pg8000.native
# from deploy_ingestion_lambda.src.errors import DatabaseConnectionError
# import boto3

# def get_secret(key):
#     sm = boto3.client('secretsmanager')
#     return sm.get_secret_value(SecretId = key)

# def get_db_password():
#     return get_secret('TOTESYS_PASSWORD')

# def get_db_name():
#     return get_secret('TOTESYS_DATABASE_NAME')

# def get_username():
#     return get_secret('TOTESYS_USERNAME')

# def get_host():
#     return get_secret('TOTESYS_HOST')

# def get_port():
#     return get_secret('TOTESYS_PORT')

# def get_region():
#     return get_secret('TOTESYS_REGION')

# def connect_to_database():
#     '''Establishes and returns a native pg8000 connection to database_name'''
#     try:
#         return  pg8000.native.Connection(
#             user=get_username(), 
#             host=get_host(), 
#             database=get_db_name(), 
#             port=get_port(), 
#             password=get_db_password()
#         )
#     except:
#         raise DatabaseConnectionError('Unable to connect to Totesys database')