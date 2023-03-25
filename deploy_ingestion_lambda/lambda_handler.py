# from deploy_ingestion_lambda.src.conn import connect_to_database
# from deploy_ingestion_lambda.src.queries import *
# from deploy_ingestion_lambda.src.errors import IngestionError
import platform
import json
import boto3
print('imported modules')

import pg8000.native
def ingest(event, context):
    print('ingest() invoked')
    # try:
    print('ingest try block entered')
    conn = connect_to_database()
    print('connection to database eastablished: ', conn)
    table_names = get_all_table_names(conn)
    for table in table_names:
        rows = create_list_of_dictionaries(conn, table)
        print(f'the first tow of {table}: {rows[0]}')
        json = list_of_dictionaries_to_json(rows)
        write_json_to_bucket(json, 'nc-de-awsome-ingestion-zone', f'totesys/{table}.json' )
    conn.close()
    # except Exception as e:
    #     raise IngestionError(f'{e}')

class AwsomeError(Exception):
    pass

class DatabaseConnectionError(AwsomeError):
    pass

class IngestionError(AwsomeError):
    pass

class WriteError(AwsomeError):
    pass

class SelectQueryError(AwsomeError):
    pass

def get_secret(key):
    sm = boto3.client('secretsmanager')
    return sm.get_secret_value(SecretId = key)

def get_db_password():
    return get_secret('TOTESYS_PASSWORD')['SecretString']

def get_db_name():
    return get_secret('TOTESYS_DATABASE_NAME')['SecretString']

def get_username():
    return get_secret('TOTESYS_USERNAME')['SecretString']

def get_host():
    return get_secret('TOTESYS_HOST')['SecretString']

def get_port():
    return get_secret('TOTESYS_PORT')['SecretString']

def get_region():
    return get_secret('TOTESYS_REGION')['SecretString']

def connect_to_database():
    '''Establishes and returns a native pg8000 connection to database_name'''
    try: 
        _user=get_username()
        print(censor_secret(_user))
    except: 
        raise DatabaseConnectionError('Unable to get_username()')
    
    try: 
        _host=get_host()
        print(censor_secret(_host))
    except: raise DatabaseConnectionError('Unable to get_host()')
    
    try :
        _database=get_db_name()
        print(censor_secret(_database))
    except:
        raise DatabaseConnectionError('Unable to get_db_name()')

    try : 
        _port=get_port()
        print(censor_secret(_port))
    except:
        raise DatabaseConnectionError('Unable to get_port()')

    try : 
        _password=get_db_password()
        print(censor_secret(_password))

    except:
        raise DatabaseConnectionError('Unable to get_password()')
    
    try:
        return  pg8000.native.Connection(
            user=_user,
            host =_host,
            database = _database,
            port = _port,
            password=_password
    #       user=get_username(), 
    #       host=get_host(), 
    #       database=get_db_name(), 
    #       port=get_port(), 
    #       password=get_db_password()
        )
    except:
        raise DatabaseConnectionError('Unable to connect to Totesys database')

def censor_secret(secret):
    length = len(secret)-3
    return f'{secret[:2]}{length*"*"}{secret[-1]}'

def get_all_table_names(conn):
    '''Returns a list of table_name strings of each table in Totesys database
    
        parameters:
            conn: pg8000.native.Connection
        
        returns:
            list of strings 
    '''
    print('get_all_table_names() invoked')
    try:
        print('get_all_table_names try block entered')
        tables = conn.run("SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema='public';")
        table_names = [table[0] for table in tables]
        print('table_names from SQL query: ', table_names)
        return table_names
    except:
        raise SelectQueryError('Unable to select table_names from totesys')

def _get_table_column_names(conn, table_name):
    '''Returns a list of column_name strings in table_name

        parameters:
            conn: pg8000.native.Connection
            table_name: string
        
        returns:
            list of strings 
    '''
    try:
        columns = conn.run(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema='public';")
        column_names = [column_name[0] for column_name in columns]
        return column_names
    except:
        raise SelectQueryError(f'Unable to get columns from {table_name}')

def _get_table_values(conn, table_name):
    '''Returns a list of lists of values in table_name
    
        parameters:
            conn: pg8000.native.Connection
            table_name: string
        
        returns:
            list of strings 
    '''
    try:
        values = conn.run(f'SELECT * FROM {table_name};')
        return values
    except:
        raise SelectQueryError(f'Unable to select values from {table_name}')

def create_list_of_dictionaries(conn, table_name):
    '''Returns a list of dicts of column/value pairs from table_name
    
        parameters:
            conn: pg8000.native.Connection
            table_name: string
        
        returns:
            list of dicts 

    '''
    columns = _get_table_column_names(conn, table_name)
    values = _get_table_values(conn, table_name)
    
    column_value_pairs = []

    for v in values:
        dict = {}
        for i in range(len(columns)):
            dict[columns[i]] = v[i]
        
        column_value_pairs.append(dict)

    return column_value_pairs

def list_of_dictionaries_to_json(list_of_dicts):
    '''Returns a (JSON) string from a list of dicts
        
        parameters:
            list_of_dicts: list of dicts

        returns:
            JSON (string)
    '''
    return json.dumps(list_of_dicts, indent=4, default=str)

def write_json_to_bucket(json, bucket_name, key):
    response = None
    try:
        s3 = boto3.client('s3')
        response = s3.put_object(Body=json, Bucket=bucket_name, Key=key)
    except:
        raise WriteError('Unable to write JSON to S3 bucket')
    return response
