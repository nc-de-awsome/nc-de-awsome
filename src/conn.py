import pg8000.native
from dotenv import load_dotenv
import os

def get_db_password(db_name):
    load_dotenv()
    lookup = {
        'totesys': 'totesys_password',
        'dw': 'dw_password'
    }   
    return os.getenv(lookup[db_name])


def get_db_name(db_name):
    load_dotenv()
    lookup = {
        'totesys': 'totesys_db_name',
        'dw': 'dw_db_name'
    }   
    return os.getenv(lookup[db_name])

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

def connect_to_database(db_name):
    return  pg8000.native.Connection(
        user=get_username(), 
        host=get_host(), 
        database=get_db_name(db_name), 
        port=get_port(), 
        password=get_db_password(db_name)
        )