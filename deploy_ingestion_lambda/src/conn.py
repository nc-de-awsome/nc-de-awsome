'''
    conn.py contains utility functions which load the required credentials to access the databases from a secrets manager/.env
'''
import pg8000.native
from dotenv import load_dotenv
import os
from deploy_ingestion_lambda.src.errors import DatabaseConnectionError

def get_db_password():
    load_dotenv()  
    return os.getenv('password')


def get_db_name():
    load_dotenv() 
    return os.getenv('db_name')

def get_username():
    load_dotenv()
    return os.getenv('username')

def get_host():
    load_dotenv()
    return os.getenv('host')

def get_port():
    load_dotenv()
    return os.getenv('port')

def get_region():
    load_dotenv()
    return os.getenv('region')

def connect_to_database():
    '''Establishes and returns a native pg8000 connection to database_name'''
    try:
        return  pg8000.native.Connection(
            user=get_username(), 
            host=get_host(), 
            database=get_db_name(), 
            port=get_port(), 
            password=get_db_password()
        )
    except:
        raise DatabaseConnectionError('Unable to connect to Totesys database')