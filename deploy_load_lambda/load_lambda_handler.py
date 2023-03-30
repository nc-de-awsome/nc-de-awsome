import pandas as pd
from datetime import datetime
import boto3
import pg8000

def load():
    conn = connect_to_database()
    
    create_fact_sales_order_table(conn)
    create_fact_purchase_order_table(conn)
    create_fact_payment_table(conn)

    create_dim_counterparty_table(conn)
    create_dim_currency_table(conn)
    create_dim_date_table(conn)
    create_dim_design_table(conn)
    create_dim_location_table(conn)
    create_dim_payment_table(conn)
    create_dim_staff_table(conn)
    create_dim_transaction_table(conn)

# create fact tables

def create_fact_sales_order_table(conn):
    conn.run("""
    DROP TABLE IF EXISTS fact_sales_order;
    
    CREATE TABLE fact_sales_order (
        sales_record_id INT PRIMARY KEY NOT NULL,
        sales_order_id INT NOT NULL,
        created_date DATE NOT NULL,
        created_time TIME NOT NULL,
        last_updated_date DATE NOT NULL,
        last_updated_time TIME NOT NULL,
        sales_staff_id INT NOT NULL,
        counterparty_id INT NOT NULL,
        units_sold INT NOT NULL,
        unit_price NUMERIC(10, 2) NOT NULL,
        currency_id INT NOT NULL,
        design_id INT NOT NULL,
        agreed_payment_date DATE NOT NULL,
        agreed_delivery_date DATE NOT NULL,
        agreed_delivery_location_id INT NOT NULL
    )
    """
)

def create_fact_purchase_order_table(conn):
    conn.run("""
    DROP TABLE IF EXISTS fact_purchase_order;
    
    CREATE TABLE IF EXISTS fact_purchase_order (
        purchase_record_id SERIAL PRIMARY KEY,
        purchase_order_id INT PRIMARY KEY,
        created_date DATE NOT NULL,
        created_time TIME NOT NULL,
        last_updated_date DATE NOT_NULL,
        last_updated_time TIME NOT_NULL,
        staff_id INT NOT NULL,
        counterparty_id INT NOT NULL,
        tem_code VARCHAR NOT NULL,
        item_quantity INT NOT NULL,
        item_unit_price NUMERIC NOT NULL,
        currency_id INT NOT NULL,
        agreed_delivery_date DATE NOT NULL,
        agreed_payment_date DATE NOT NULL,
        agreed_delivery_location_id INT NOT NULL
    )
    """
)
    
def create_fact_payment_table(conn):
    conn.run("""
    DROP TABLE IF EXISTS fact_payment;

    CREATE TABLE fact_payment (
        payment_record_id PRIMARY SERIAL NUMBER,
        payment_id INT NOT NULL,
        created_date DATE NOT NULL,
        created_time TIME NOT NULL,
        last_updated_date DATE NOT NULL,
        last_updated_time TIME NOT NULL,
        transaction_id INT NOT NULL,
        counterparty_id INT NOT NULL,
        payment_amount NUMERIC NOT NULL,
        currency_id INT NOT NULL,
        payment_type_id INT NOT NULL,
        paid BOOLEAN NOT NULL,
        payment_date DATE NOT NULL

    )"""
)
    
# create dim tables

def create_dim_counterparty_table(conn):
    conn.run("""
        DROP TABLE IF EXISTS dim_counterparty;
        
        CREATE TABLE dim_counterparty (
            counterparty_id INT PRIMARY KEY NOT NULL,
            counterparty_legal_name VARCHAR NOT NULL,
            counterparty_legal_address_line_1 VARCHAR NOT NULL,
            counterparty_legal_address_line2 VARCHAR,
            counterparty_legal_district VARCHAR,
            counterparty_legal_city VARCHAR NOT NULL,
            counterparty_legal_postal_code VARCHAR NOT NULL,
            counterparty_legal_country VARCHAR NOT NULL,
            counterparty_legal_phone_number VARCHAR NOT NULL
    )"""
)

def create_dim_currency_table(conn):
    conn.run("""
        DROP TABLE IF EXISTS dim_currency;
            
        CREATE TABLE dim_currency (
            currency_id INT PRIMARY KEY NOT NULL,
            currency_code VARCHAR NOT NULL,
            currency_name VARCHAR NOT NULL
        )"""
)


def create_dim_date_table(conn):
    conn.run("""
        DROP TABLE IF EXISTS dim_date;
        
        CREATE TABLE dim_date (
            date_id INT PRIMARY KEY NOT NULL,
            year INT NOT NULL,
            month INT NOT NULL,
            day INT NOT NULL,
            day_of_week INT NOT NULL,
            day_name VARCHAR NOT NULL,
            month_name VARCHAR NOT NULL,
            quarter int NOT NULL
        )""" 
)


def create_dim_design_table(conn):
    conn.run("""
    DROP TABLE IF EXISTS dim_design;

    CREATE TABLE dim_design (
        design_id INT PRIMARY KEY NOT NULL,
        design_name VARCHAR NOT NULL,
        file_location VARCHAR NOT NULL,
        file_name VARCHAR NOT NULL
    )"""
)

def create_dim_location_table(conn):
    conn.run(""" 
    DROP TABLE IF EXISTS dim_location;

    CREATE TABLE dim_location (
        location_id INT PRIMARY KEY NOT NULL,
        address_line_1 VARCHAR NOT NULL,
        address_line_2 VARCHAR,
        district VARCHAR,
        city VARCHAR NOT NULL,
        postal_code VARCHAR NOT NULL,
        country VARCHAR NOT NULL,
        phone VARCHAR NOT NULL
    )"""
)
    
def create_dim_payment_table(conn):
    conn.run("""
    DROP TABLE IF EXISTS dim_payment;

    CREATE TABLE dim_payment (
        payment_type_id INT PRIMARY KEY NOT NULL,
        payment_type_name VARCHAR NOT NULL
    )"""
)

def create_dim_staff_table(conn):
    conn.run("""
    DROP TABLE IF EXISTS dim_staff;
    
    CREATE TABLE dim_staff (
        staff_id INT PRIMARY KEY NOT NULL,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        department_name VARCHAR NOT NULL,
        location VARCHAR NOT NULL,
        email_address VARCHAR NOT NULL
    )"""
)

def create_dim_transaction_table(conn):
    conn.run("""
    DROP TABLE IF EXISTS dim_transaction;
    
    CREATE TABLE dim_transaction (
        transaction_id INT PRIMARY KEY NOT NULL,
        transaction_type VARCHAR NOT NULL,
        sales_order_id INT,
        purchase_order_id INT
    )"""
)


# insert values




# connection to database

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
        raise DatabaseConnectionError('Unable to connect to DW database')

def get_secret(key):
    sm = boto3.client('secretsmanager')
    secret = sm.get_secret_value(SecretId = key)
    return secret['SecretString']

def get_db_password():
    return get_secret('DW_PASSWORD')

def get_db_name():
    return get_secret('DW_DATABASE_NAME')

def get_username():
    return get_secret('DW_USERNAME')

def get_host():
    return get_secret('DW_HOST')

def get_port():
    return get_secret('DW_PORT')

def get_region():
    return get_secret('DW_REGION')

# utils

def load_data_frame_from_parquet_file(filename):
    return pd.read_parquet(f"./transformation_parquet/dim_{filename}.parquet")

def dataframe_to_list_of_row_values(data_frame):
    return data_frame.to_numpy().tolist()

# errors

class AwsomeError(Exception):
    pass

class DatabaseConnectionError(AwsomeError):
    pass


class WriteError(AwsomeError):
    pass
