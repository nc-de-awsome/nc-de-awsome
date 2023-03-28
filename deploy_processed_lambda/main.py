import pandas as pd
import requests
import json
import os
from datetime import datetime
import boto3
import io


def transform(event, context):
    # load all data from transformation bucket
    staff_df = load_data_frame_from_json('staff')
    department_df = load_data_frame_from_json('department')
    design_df = load_data_frame_from_json('design')
    address_df = load_data_frame_from_json('address')
    counterparty_df = load_data_frame_from_json('counterparty')
    sales_order_df = load_data_frame_from_json('sales_order')
    currency_df = load_data_frame_from_json('currency')
    payment_df = load_data_frame_from_json('payment')
    transaction_df = load_data_frame_from_json('transaction')

    # get/load other data
    currency_name_df = load_data_frame_from_csv('./other_data/currencies.csv')
    # update_forex_rates()

    # transform data into fact and dim tables
    dim_staff = generate_dim_staff(staff_df, department_df)
    dim_design = generate_dim_design(design_df)
    dim_location = generate_dim_location(address_df)
    dim_counterparty = generate_dim_counterparty(counterparty_df, address_df)
    dim_date = generate_dim_date()
    dim_currency = generate_dim_currency(currency_df, currency_name_df)
    dim_payment = generate_dim_payment_type(payment_df, transaction_df)
    dim_transaction = generate_dim_transaction(transaction_df)
    fact_purchase_order = generate_fact_purchase_order()
    fact_payment = generate_fact_payment()


    # writeout fact/dim tables to parquet to load bucket
    write_data_frame_to_parquet(dim_staff, 'dim_staff')
    write_data_frame_to_parquet(dim_design, 'dim_design')
    write_data_frame_to_parquet(dim_location, 'dim_location')
    write_data_frame_to_parquet(dim_counterparty, 'dim_counterparty')
    write_data_frame_to_parquet(dim_date, 'dim_date')
    write_data_frame_to_parquet(dim_currency, 'dim_currency')
    write_data_frame_to_parquet(dim_payment, 'dim_payment')
    write_data_frame_to_parquet(dim_transaction, 'dim_transaction')
    write_data_frame_to_parquet(fact_purchase_order, 'fact_purchase_order')
    write_data_frame_to_parquet(fact_payment, 'fact_payment')

def generate_dim_staff(staff_df, department_df):
    return staff_df.join(
        department_df.set_index('department_id'),
        on = 'department_id',
        lsuffix='_L'
    )[
        [
            'staff_id',
            'first_name',
            'last_name',
            'department_name',
            'location',
            'email_address'
        ]
    ]

def generate_dim_design(design_df):
    return design_df[
        [
            'design_id',
            'design_name',
            'file_location',
            'file_name'
        ]
    ]

def generate_dim_location(address_df):
    return address_df[
        [
            'address_id', 
            'address_line_1', 
            'address_line_2', 
            'district', 
            'city', 
            'postal_code', 
            'country',
            'phone'
        ]
    ].rename(
        columns={
            'address_id' : 'location_id'
        }
    )

def generate_dim_counterparty(counterparty_df, address_df):
    return counterparty_df.join(
        address_df.set_index('address_id'),
        on = 'legal_address_id',
        lsuffix='_L',
    )[
        [
            'counterparty_id',
            'counterparty_legal_name', 
            'address_line_1',
            'address_line_2',
            'district',
            'city',
            'postal_code',
            'country',
            'phone'
        ]
    ].rename(
        columns={
            'address_line_1' : 'counterparty_legal_address_line_1',
            'address_line_2' : 'counterparty_legal_address_line_2',
            'district' : 'counterparty_legal_district',
            'city' : 'counterparty_legal_city',
            'postal_code' :'counterparty_legal_postal_code',
            'country' : 'counterparty_legal_country',
            'phone' : 'counterparty_legal_phone_number'
        }
    )

def generate_dim_currency(currency_df, currency_name_df):
    return currency_df.join(
        currency_name_df.set_index('CurrencyCode'),
        on='currency_code'
    )[
        [
            'currency_id',
            'currency_code',
            'CurrencyName'
        ]
    ].rename(
        columns={
            'CurrencyName' : 'currency_name'
        }
    )

def generate_dim_payment_type(payment_df, transaction_df):
    return payment_df.join(
        transaction_df,
        on='transaction_id',
        lsuffix='_L'
    )[
        [
            'payment_type_id',
            'transaction_type',
        ]
    ].rename(
        columns={
            'transaction_type' : 'payment_type_name'
        }
    )

def generate_dim_transaction(transaction_df):
    
    return transaction_df.fillna(0)[
        [
            'transaction_id',
            'transaction_type',
            'sales_order_id',
            'purchase_order_id'
        ]
    ][
        [
            'sales_order_id',
            'purchase_order_id'
        ]
    ].astype(int)

def update_forex_rates():
    '''Gets forex rates data, writes to file, and updates at approx 8am each day'''
    forex_log_path = './other_data/forex_rates_log.json'
    
    now = datetime.now()

    try:
        if os.path.exists(forex_log_path):
            with open(forex_log_path, 'r') as f:
                forex = json.loads(f.read())
                last_check = datetime.utcfromtimestamp(forex['last_updated'])

                if abs(now.day-last_check.day) == 0 or now.hour < 8 :
                    print('No need to update forex rates')
                    return
    except:
        print('Could not find/read forex rate log; will get forex rates')
    
    currency_pairs=[
        'GBPUSD',
        'EURGBP',
        'EURUSD',
        'USDEUR',
        'USDGBP',
    ]
    
    rates = []
    for cp in currency_pairs:
        response =requests.get(f'https://www.freeforexapi.com/api/live?pairs={cp}')
        rate = json.loads(response.text)['rates']
        dict = {cp : rate[cp]['rate'] }
        rates.append(dict)

    with open('./other_data/forex_rates.json', 'w') as f:
        f.write(json.dumps(rates, indent=4))
    
    with open(f'{forex_log_path}', 'w') as f:
        info =   {'last_updated':now.timestamp()}
        f.write(json.dumps(info))
    
    print('Updated forex rates')

# utilities

def load_data_frame_from_json(table_name):
    return pd.read_json(f'{s3_file_reader(table_name)}')

def load_data_frame_from_csv(filepath):
    return pd.read_csv(f'{filepath}')

def write_data_frame_to_parquet(data_frame, file_name):
    # data_frame.to_parquet(
    #     f's3://nc-de-awsome-processed-zone/transformation_parquet/{file_name}.parquet', 
    #     engine='auto', 
    #     compression=None, 
    #     index=False
    # )
    parquet_buffer = io.BytesIO()
    data_frame.to_parquet(parquet_buffer, index=False)
    parquet_buffer.seek(0)
    s3 = boto3.client('s3')
    s3.upload_fileobj(parquet_buffer, 'nc-de-awsome-processed-zone', f'transformation_parquet/{file_name}.parquet')

##################### temp code #####################
    # write_data_frame_to_local_txt(data_frame, file_name)

##################### temp code #####################
def write_data_frame_to_local_txt(data_frame, file_name):
    with open(f'./transformation_parquet/{file_name}.txt', 'w') as f:
        f.write(data_frame.to_string())

def generate_dim_date():
    df = pd.DataFrame(pd.date_range('1/1/1999','12/31/2023'), columns=['date'])
    df['date_id'] = df['date']
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.strftime("%A")
    df['month_name'] = df['date'].dt.strftime("%B")
    df['quarter'] = df['date'].dt.quarter

    return df


def generate_fact_purchase_order():
    fact_purchase = load_data_frame_from_json('purchase_order')

    fact_purchase['created_date'] = fact_purchase['created_at'].dt.date
    fact_purchase['created_time'] = fact_purchase['created_at'].dt.time
    fact_purchase.drop('created_at', axis=1, inplace=True)

    fact_purchase['last_updated'] = pd.to_datetime(fact_purchase['last_updated'])
    fact_purchase['last_updated_date'] = fact_purchase['last_updated'].dt.date
    fact_purchase['last_updated_time'] = fact_purchase['last_updated'].dt.time
    fact_purchase.drop('last_updated', axis=1, inplace=True)
    fact_purchase['purchase_record_id'] = fact_purchase.index + 1
    

    return fact_purchase


def generate_fact_payment():
    fact_payment = load_data_frame_from_json('payment')
    fact_payment['created_date'] = fact_payment['created_at'].dt.date
    fact_payment['created_time'] = fact_payment['created_at'].dt.time
    fact_payment.drop('created_at', axis=1, inplace=True)

    fact_payment['last_updated'] = pd.to_datetime(fact_payment['last_updated'])
    fact_payment['last_updated_date'] = fact_payment['last_updated'].dt.date
    fact_payment['last_updated_time'] = fact_payment['last_updated'].dt.time
    fact_payment.drop('last_updated', axis=1, inplace=True)

    fact_payment.drop(['counterparty_ac_number', 'company_ac_number'], axis=1, inplace=True)
    fact_payment['payment_record_id'] = fact_payment.index + 1

    return fact_payment

def fetch_log_timestamp():
    client = boto3.client('s3')
    time_query = client.get_object(Bucket= 'nc-de-awsome-ingestion-zone', Key='query_log.json')
    return time_query

# print(fetch_log_timestamp()['Body'].read().decode())

def s3_file_reader(table_name):
    response = None
    try:
        client = boto3.client('s3')
        response = client.get_object(
            Bucket= 'nc-de-awsome-ingestion-zone',
            Key= f'totesys/23-03-28 06:07:23/{table_name}.json'
        )
    except Exception:
        raise ReadError('Unable to read JSON from s3 bucket')
    return response['Body'].read().decode()

currency_df = load_data_frame_from_json('staff')
write_data_frame_to_parquet(currency_df, 'staff')

# Errors - CHANGE
# failure to read/access 
# write error

class AwsomeError(Exception):
    pass

class TransformationError(AwsomeError):
    pass

class WriteError(AwsomeError):
    pass

class ReadError(AwsomeError):
    pass