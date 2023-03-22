'''
    conn.py contains utility functions which load the required credentials to access the databases from a secrets manager/.env
'''
import pg8000.native
from dotenv import load_dotenv
import os

def get_db_password(database_name):
    '''Returns the password for database_name'''
    load_dotenv()
    lookup = {
        'totesys': 'totesys_password',
        'dw': 'dw_password'
    }   
    return os.getenv(lookup[database_name])


def get_db_name(database_name):
    '''Returns the database name for database_name'''
    load_dotenv()
    lookup = {
        'totesys': 'totesys_db_name',
        'dw': 'dw_db_name'
    }   
    return os.getenv(lookup[database_name])

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

def connect_to_database(database_name):
    '''Establishes and returns a native pg8000 connection to database_name'''
    return  pg8000.native.Connection(
        user=get_username(), 
        host=get_host(), 
        database=get_db_name(database_name), 
        port=get_port(), 
        password=get_db_password(database_name)
    )