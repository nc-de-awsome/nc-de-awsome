import pandas as pd
from datetime import datetime
import boto3
import pg8000
import io


def load(event, context):
    conn = connect_to_database()
    start_time = datetime.now()
    print(start_time)
    #deleting data in fact tables
    conn.run('DELETE FROM fact_payment;')
    conn.run('DELETE FROM fact_sales_order;')
    conn.run('DELETE FROM fact_purchase_orders;')


    print('Loading parquet from s3')
    dim_counterparty_df = load_data_frame_from_parquet_file('dim_counterparty')
    dim_currency_df = load_data_frame_from_parquet_file('dim_currency')
    dim_date_df = load_data_frame_from_parquet_file('dim_date')
    dim_design_df = load_data_frame_from_parquet_file('dim_design')
    dim_location_df = load_data_frame_from_parquet_file('dim_location') 
    dim_payment_df = load_data_frame_from_parquet_file('dim_payment_type')
    dim_staff_df = load_data_frame_from_parquet_file('dim_staff')
    dim_transaction_df = load_data_frame_from_parquet_file('dim_transaction')
    fact_sales_df = load_data_frame_from_parquet_file('fact_sales_order')
    fact_purchase_df = load_data_frame_from_parquet_file('fact_purchase_order')
    fact_payment_df = load_data_frame_from_parquet_file('fact_payment')
    fact_sales_df.drop('sales_record_id', axis=1, inplace=True)
    fact_purchase_df.drop('purchase_record_id', axis=1, inplace=True)
    fact_payment_df.drop('payment_record_id', axis=1, inplace=True)
    
    print('converting pdataframe to nested lists')
    counterpart_list = dataframe_to_list_of_row_values(dim_counterparty_df)
    currency_list = dataframe_to_list_of_row_values(dim_currency_df)
    date_list = dataframe_to_list_of_row_values(dim_date_df)
    design_list = dataframe_to_list_of_row_values(dim_design_df)
    location_list = dataframe_to_list_of_row_values(dim_location_df)
    payment_list = dataframe_to_list_of_row_values(dim_payment_df)
    staff_list = dataframe_to_list_of_row_values(dim_staff_df)
    transaction_list = dataframe_to_list_of_row_values(dim_transaction_df)
    fact_sales_list = dataframe_to_list_of_row_values(fact_sales_df)
    fact_purchase_list = dataframe_to_list_of_row_values(fact_purchase_df)
    fact_payment_list = dataframe_to_list_of_row_values(fact_payment_df)
    
    print('now inserting to database')
    insert_dim_counterparty_to_dw(conn, counterpart_list)
    insert_dim_currency_to_dw(conn, currency_list)
    insert_dim_date_to_dw(conn, date_list)
    insert_dim_design_to_dw(conn, design_list)
    insert_dim_location_to_dw(conn, location_list)
    insert_dim_payment_to_dw(conn, payment_list)
    insert_dim_staff_to_dw(conn, staff_list)
    insert_dim_transaction_to_dw(conn, transaction_list)
    print('inserting facts now')
    insert_fact_sales_order_to_dw(conn, fact_sales_list)
    insert_fact_payment_order_to_dw(conn, fact_payment_list)
    insert_fact_purchase_to_dw(conn, fact_purchase_list)

    conn.close()
    end_time = datetime.now()
    print(end_time)
    print(end_time - start_time, '<--- time elapsed')
    print('load lambda complete')

# errors

class AwsomeError(Exception):
    pass

class DatabaseConnectionError(AwsomeError):
    pass


class WriteError(AwsomeError):
    pass

class ReadError(AwsomeError):
    pass

# create fact tables

def create_fact_sales_order_table(conn):
    conn.run("""
    DROP TABLE IF EXISTS fact_sales_order;
    
    CREATE TABLE fact_sales_order (
        sales_record_id INT PRIMARY KEY NOT NULL,
        sales_order_id INT NOT NULL,
        created_date DATE NOT NULL REFERENCES dim_date(date_id),
        created_time TIME NOT NULL,
        last_updated_date DATE NOT NULL REFERENCES dim_date(date_id),
        last_updated_time TIME NOT NULL,
        sales_staff_id INT NOT NULL REFERENCES dim_staff(staff_id),
        counterparty_id INT NOT NULL REFERENCES dim_counterparty(counterparty_id),
        units_sold INT NOT NULL,
        unit_price NUMERIC(10, 2) NOT NULL,
        currency_id INT NOT NULL REFERENCES dim_currency(currency_id),
        design_id INT NOT NULL REFERENCES dim_design(design_id),
        agreed_payment_date DATE NOT NULL REFERENCES dim_date(date_id),
        agreed_delivery_date DATE NOT NULL REFERENCES dim_date(date_id),
        agreed_delivery_location_id INT NOT NULL REFERENCES dim_location(location_id)
    );
    """
)

def create_fact_purchase_order_table(conn):
    conn.run("""
    DROP TABLE IF EXISTS fact_purchase_order;
    
    CREATE TABLE IF EXISTS fact_purchase_order (
        purchase_record_id SERIAL PRIMARY KEY,
        purchase_order_id INT,
        created_date DATE NOT NULL REFERENCES dim_date(date_id),
        created_time TIME NOT NULL ,
        last_updated_date DATE NOT_NULL REFERENCES dim_date(date_id),
        last_updated_time TIME NOT_NULL,
        staff_id INT NOT NULL REFERENCES dim_staff(staff_id),
        counterparty_id INT NOT NULL REFERENCES dim_counterparty(counterparty_id),
        item_code VARCHAR NOT NULL,
        item_quantity INT NOT NULL,
        item_unit_price NUMERIC NOT NULL,
        currency_id INT NOT NULL REFERENCES dim_currency(currency_id),
        agreed_delivery_date DATE NOT NULL REFERENCES dim_date(date_id),
        agreed_payment_date DATE NOT NULL REFERENCES dim_date(date_id),
        agreed_delivery_location_id INT NOT NULL REFERENCES dim_location(location_id)
    );
    """
)

def create_fact_payment_table(conn):
    conn.run("""
    DROP TABLE IF EXISTS fact_payment;
    CREATE TABLE fact_payment (
        payment_record_id PRIMARY SERIAL NUMBER,
        payment_id INT NOT NULL,
        created_date DATE NOT NULL REFERENCES dim_date(date_id),
        created_time TIME NOT NULL,
        last_updated_date DATE NOT NULL REFERENCES dim_date(date_id),
        last_updated_time TIME NOT NULL,
        transaction_id INT NOT NULL REFERENCES dim_transaction(transaction_id),
        counterparty_id INT NOT NULL REFERENCES dim_counterparty(counterparty_id),
        payment_amount NUMERIC NOT NULL,
        currency_id INT NOT NULL REFERENCES dim_currency(currency_id),
        payment_type_id INT NOT NULL REFERENCES dim_payment_type(payment_type_id),
        paid BOOLEAN NOT NULL,
        payment_date DATE NOT NULL REFERENCES dim_date(date_id)
    );
    """
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
        return  pg8000.connect(
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

def load_data_frame_from_parquet_file(table_name):
    df = None
    try:
        buffer = io.BytesIO()
        client = boto3.resource('s3')
        response = client.Object(
            'nc-de-awsome-processed-zone',
            f'transformation_parquet/{table_name}.parquet'
        )
        response.download_fileobj(buffer)
        df = pd.read_parquet(buffer)
    except Exception:
        raise ReadError('Unable to read Parquet from s3 bucket')
    return df
        
    

def dataframe_to_list_of_row_values(data_frame):
    return data_frame.values.tolist()

# insert values
def insert_dim_counterparty_to_dw(conn, data):
    cursor = conn.cursor()
    sql = '''INSERT INTO dim_counterparty (
            counterparty_id,
            counterparty_legal_name,
            counterparty_legal_address_line_1,
            counterparty_legal_address_line_2,
            counterparty_legal_district,
            counterparty_legal_city,
            counterparty_legal_postal_code,
            counterparty_legal_country,
            counterparty_legal_phone_number    
    ) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'''
    conn.run('DELETE FROM dim_counterparty;')
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()

def insert_dim_currency_to_dw(conn, data):
    cursor = conn.cursor()
    sql = '''INSERT INTO dim_currency (
            currency_id,
            currency_code,
            currency_name)
            VALUES (%s, %s, %s);'''
    conn.run('DELETE FROM dim_currency;')
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()

def insert_dim_date_to_dw(conn,data):
    cursor = conn.cursor()
    sql = '''INSERT INTO dim_date (
        date_id, 
        year, 
        month, 
        day, 
        day_of_week, 
        day_name, 
        month_name, 
        quarter) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'''
    conn.run('DELETE FROM dim_date;')
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()

def insert_dim_design_to_dw(conn,data):
    cursor = conn.cursor()
    sql = '''INSERT INTO dim_design (
            design_id, 
            design_name, 
            file_location, 
            file_name)  
            VALUES (%s, %s, %s, %s);'''
    conn.run('DELETE FROM dim_design;')
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()   

def insert_dim_location_to_dw(conn, data):
    cursor = conn.cursor()
    sql = '''INSERT INTO dim_location (
            location_id,
            address_line_1,
            address_line_2,
            district,
            city,
            postal_code,
            country,
            phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'''
    conn.run('DELETE FROM dim_location;')
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()

def insert_dim_payment_to_dw(conn, data):
    cursor = conn.cursor()
    sql = '''INSERT INTO dim_payment_type (
            payment_type_id,
            payment_type_name)
            VALUES (%s, %s);'''
    conn.run('DELETE FROM dim_payment_type;')
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()    

def insert_dim_staff_to_dw(conn, data):
    cursor = conn.cursor()
    sql = '''INSERT INTO dim_staff (
            staff_id,
            first_name,
            last_name,
            department_name,
            location,
            email_address)
            VALUES (%s, %s, %s, %s, %s, %s);'''
    conn.run('DELETE FROM dim_staff;')
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()

def insert_dim_transaction_to_dw(conn, data):
    cursor = conn.cursor()
    sql = '''INSERT INTO dim_transaction (
            transaction_id,
            transaction_type,
            sales_order_id,
            purchase_order_id)
            VALUES (%s, %s, %s, %s);'''
    conn.run('DELETE FROM dim_transaction;')
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()

def insert_fact_purchase_to_dw(conn, data):
    cursor = conn.cursor()
    sql = '''INSERT INTO fact_purchase_orders (
            purchase_order_id,
            created_date,
            created_time,
            last_updated_date,
            last_updated_time,
            staff_id,
            counterparty_id,
            item_code,
            item_quantity,
            item_unit_price,
            currency_id,
            agreed_delivery_date,
            agreed_payment_date,
            agreed_delivery_location_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()

def insert_fact_sales_order_to_dw(conn, data):
    cursor = conn.cursor()
    sql = '''INSERT INTO fact_sales_order (
            sales_order_id,
            created_date,
            created_time,
            last_updated_date,
            last_updated_time,
            sales_staff_id,
            counterparty_id,
            units_sold,
            "unit price",
            currency_id,
            design_id,
            agreed_payment_date,
            agreed_delivery_date,
            agreed_delivery_location_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()    
    

def insert_fact_payment_order_to_dw(conn, data):
    cursor = conn.cursor()
    sql = '''INSERT INTO fact_payment (
            payment_id,
            created_date,
            created_time,
            last_updated_date,
            last_updated,
            transaction_id,
            counterparty_id,
            payment_amount,      
            currency_id,
            payment_type_id,
            paid,
            payment_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()

# print(connect_to_database().run('SELECT * FROM fact_purchase_orders limit 1'))

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
            AND table_schema='project_team_2';
            """
        )
        column_names = [column_name[0] for column_name in columns]
        return column_names
    except:
        raise DatabaseConnectionError(f'Unable to get columns from {table_name}')

# print(_get_table_column_names(connect_to_database(), 'fact_sales_order'))

