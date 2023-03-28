import json
import boto3
from datetime import datetime
import pg8000.native
import pytz

def ingest(event, context):
    try:
        conn = connect_to_database()
        table_names = get_all_table_names(conn)
        time_of_query = get_time_of_query()
        for table in table_names:
            rows = create_list_of_dictionaries(conn, table)
            json_data = list_of_dictionaries_to_json(rows)
            write_json_to_bucket(
                json_data,
                'nc-de-awsome-ingestion-zone',
                f'totesys/{time_of_query}/{table}.json' 
            )
            log_timestamp = create_log_timestamp(time_of_query)
            json_time = json.dumps(log_timestamp, indent=4, default=str)
            write_json_to_bucket(
                json_time,
                'nc-de-awsome-ingestion-zone',
                f'query_log.json' 
            )
        conn.close()
        print(f'Ingestion @{time_of_query} complete.')
    except Exception as e:
        raise IngestionError(f'{e}')

def connect_to_database():
    '''Establishes and returns a native pg8000 connection to database_name'''
    try: 
        _user=get_username()
    except: raise DatabaseConnectionError('Unable to get_username()')
    
    try: 
        _host=get_host()
    except: raise DatabaseConnectionError('Unable to get_host()')
    
    try :
        _database=get_db_name()
    except: raise DatabaseConnectionError('Unable to get_db_name()')

    try : 
        _port=get_port()
    except: raise DatabaseConnectionError('Unable to get_port()')

    try : 
        _password=get_db_password()
    except:
        raise DatabaseConnectionError('Unable to get_password()')
    
    try:
        return  pg8000.native.Connection(
            user=_user,
            host =_host,
            database = _database,
            port = _port,
            password=_password
        )
    except:
        raise DatabaseConnectionError('Unable to connect to Totesys database')

def get_secret(key):
    sm = boto3.client('secretsmanager')
    secret = sm.get_secret_value(SecretId = key)
    return secret['SecretString']

def get_db_password():
    return get_secret('TOTESYS_PASSWORD')

def get_db_name():
    return get_secret('TOTESYS_DATABASE_NAME')

def get_username():
    return get_secret('TOTESYS_USERNAME')

def get_host():
    return get_secret('TOTESYS_HOST')

def get_port():
    return get_secret('TOTESYS_PORT')

def get_region():
    return get_secret('TOTESYS_REGION')

def get_all_table_names(conn):
    '''Returns a list of table_name strings of each table in Totesys database
    
        parameters:
            conn: pg8000.native.Connection
        
        returns:
            list of strings 
    '''
    try:
        tables = conn.run("""
            SELECT table_name FROM information_schema.tables
            WHERE table_type='BASE TABLE' AND table_schema='public';
        """
        )
        table_names = [table[0] for table in tables]
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
        columns = conn.run(f"""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = '{table_name}'
            AND table_schema='public';
            """
        )
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
    try:
        s3 = boto3.client('s3')
        s3.put_object(Body=json.encode("utf-8"), Bucket=bucket_name, Key=key)
    except:
        raise WriteError('Unable to write JSON to S3 bucket')

def get_time_of_query():
    tz = pytz.timezone('Europe/London')
    now = datetime.now(tz).strftime('%y-%m-%d %H:%M:%S')
    return now

def create_log_timestamp(time_of_query):
    obj = {
        "Last successful query" : time_of_query
        # "Last query" : time_of_query,
    }

# Errors

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

datetime.utcnow().strftime('%y-%m-%d %H:%M:%S')
