import pandas as pd
# import requests
import json
import os
from datetime import datetime
import boto3
import io
import pytz

def transform(event, context):
    try:
        # load all data from transformation bucket
        staff_df = load_data_frame_from_json('staff')
        department_df = load_data_frame_from_json('department')
        design_df = load_data_frame_from_json('design')
        address_df = load_data_frame_from_json('address')
        counterparty_df = load_data_frame_from_json('counterparty')
        currency_df = load_data_frame_from_json('currency')
        payment_df = load_data_frame_from_json('payment')
        transaction_df = load_data_frame_from_json('transaction') 
        payment_type_df = load_data_frame_from_json('payment_type')
        sales_order_df = load_data_frame_from_json('sales_order')
        purchase_order_df = load_data_frame_from_json('purchase_order')

        # get/load other data
        currency_name_df = load_data_frame_from_csv('./other_data/currencies.csv')
        # update_forex_rates()

        # transform data into fact and dim tables
        print('1')
        dim_staff = generate_dim_staff(staff_df, department_df)
        print('2')
        dim_design = generate_dim_design(design_df)
        print('3')
        dim_location = generate_dim_location(address_df)
        print('4')
        dim_counterparty = generate_dim_counterparty(counterparty_df, address_df)
        print('5')
        dim_date = generate_dim_date(sales_order_df)
        print('6')
        dim_currency = generate_dim_currency(currency_df, currency_name_df)
        print('7')
        dim_payment_type = generate_dim_payment_type(payment_type_df)
        print('8')
        dim_transaction = generate_dim_transaction(transaction_df)
        print('9')

        fact_purchase_order = generate_fact_purchase_order(purchase_order_df)
        print('10')
        fact_payment = generate_fact_payment(payment_df)
        print('11')
        fact_sales_order = generate_fact_sales_order(sales_order_df)

        # writeout fact/dim tables to parquet to load bucket
        print('12')
        write_data_frame_to_parquet(dim_staff, 'dim_staff')
        print('13')
        write_data_frame_to_parquet(dim_design, 'dim_design')
        print('14')
        write_data_frame_to_parquet(dim_location, 'dim_location')
        print('15')
        write_data_frame_to_parquet(dim_counterparty, 'dim_counterparty')
        print('16')
        write_data_frame_to_parquet(dim_date, 'dim_date')
        print('17')
        write_data_frame_to_parquet(dim_currency, 'dim_currency')
        print('18')
        write_data_frame_to_parquet(dim_payment_type, 'dim_payment_type')
        print('19')
        write_data_frame_to_parquet(dim_transaction, 'dim_transaction')
        print('20')
        write_data_frame_to_parquet(fact_purchase_order, 'fact_purchase_order')
        print('21')
        write_data_frame_to_parquet(fact_payment, 'fact_payment')
        print('22')
        write_data_frame_to_parquet(fact_sales_order, 'fact_sales_order')
        print('23')
        
        print('write df to parquet complete')
        time_query = get_time_of_query()
        print('passed get_time_query')
        log_timestamp = create_log_timestamp(time_query)
        print('log stamp created')
        json_time = json.dumps(log_timestamp, indent=4, default=str)
        write_json_to_bucket(
                json_time,
                'nc-de-awsome-processed-zone',
                f'query_log.json' 
            )
        print(f'Transformation @{time_query} complete.')
    except Exception as e:
        raise TransformationError(f'{e}')

# dim tables

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

def generate_dim_payment_type(payment_type_df):
    return payment_type_df[
            [
                'payment_type_id',
                'payment_type_name',
            ]
    ]

def generate_dim_date(sales_order_df):
    sales_timestamps=sales_order_df[
        [
            'created_at'
        ]
    ]

    def create_datetime(timestamp):
        return pd.to_datetime(
            pd.Timestamp(timestamp).
            to_pydatetime().
            replace(microsecond=0)
        )

    dicts = []
    datetimes = [create_datetime(s[0]) for s in sales_timestamps.to_numpy()]
    for date in datetimes:
        dicts.append(
                {
                    'date_id' : date.date(),
                    'year' : date.year,
                    'month' : date.month,
                    'day' : date.day,
                    'day_of_week' : date.day_of_week,
                    'day_name' : date.day_name(),
                    'month_name' : date.month_name(),
                    'quarter' : date.quarter
            }
        )
    return pd.DataFrame.from_records(dicts).drop_duplicates(keep='first')

def generate_dim_transaction(transaction_df):
    
    return transaction_df.fillna(0)[
        [
            'transaction_id',
            'transaction_type',
            'sales_order_id',
            'purchase_order_id'
        ]
    ].astype(
        {
            'transaction_id': 'int64',
            'transaction_type': 'object',
            'sales_order_id': 'int64',
            'purchase_order_id': 'int64'
        }
    )

# fact tables

def generate_fact_purchase_order(purchase_order_df):

    purchase_order_df['created_date'] = purchase_order_df['created_at'].dt.date
    purchase_order_df['created_time'] = purchase_order_df['created_at'].dt.time
    purchase_order_df.drop('created_at', axis=1, inplace=True)

    purchase_order_df['last_updated'] = pd.to_datetime(purchase_order_df['last_updated'])
    purchase_order_df['last_updated_date'] = purchase_order_df['last_updated'].dt.date
    purchase_order_df['last_updated_time'] = purchase_order_df['last_updated'].dt.time
    purchase_order_df.drop('last_updated', axis=1, inplace=True)
    purchase_order_df['purchase_record_id'] = purchase_order_df.index + 1
    
    purchase_order_df['agreed_delivery_date'] = pd.to_datetime(purchase_order_df['agreed_delivery_date']).dt.date
    purchase_order_df['agreed_payment_date'] = pd.to_datetime(purchase_order_df['agreed_payment_date']).dt.date
    return purchase_order_df.reindex(columns=[
            "purchase_record_id",
            "purchase_order_id",
            "created_date",
            "created_time",
            "last_updated_date",
            "last_updated_time",
            "staff_id",
            "counterparty_id",
            "item_code",
            "item_quantity",
            "item_unit_price",
            "currency_id",
            "agreed_delivery_date",
            "agreed_payment_date",
            "agreed_delivery_location_id"
        ]
    )

def generate_fact_payment(payment_df):
    payment_df['payment_record_id'] = payment_df.index + 1
    payment_df['created_date'] = payment_df['created_at'].dt.date
    payment_df['created_time'] = payment_df['created_at'].dt.time
    payment_df.drop('created_at', axis=1, inplace=True)

    payment_df['last_updated'] = pd.to_datetime(payment_df['last_updated'])
    payment_df['last_updated_date'] = payment_df['last_updated'].dt.date
    payment_df['last_updated_time'] = payment_df['last_updated'].dt.time
    payment_df.drop('last_updated', axis=1, inplace=True)
    payment_df['payment_date'] = pd.to_datetime(payment_df['payment_date']).dt.date

    payment_df.drop(['counterparty_ac_number', 'company_ac_number'], axis=1, inplace=True)

    return payment_df.reindex(columns=[
        'payment_record_id',
        'payment_id',
        'created_date',
        'created_time',
        'last_updated_date',
        'last_updated_time',
        'transaction_id',
        'counterparty_id',
        'payment_amount',
        'currency_id',
        'payment_type_id',
        'paid',
        'payment_date'
    ]
    )

def generate_fact_sales_order(sales_order_df):
    sales_order_df['sales_record_id'] = sales_order_df.index + 1
    sales_order_df['created_date'] = sales_order_df['created_at'].dt.date
    sales_order_df['created_time'] = sales_order_df['created_at'].dt.time
    sales_order_df['last_updated'] = pd.to_datetime(sales_order_df['last_updated'])
    sales_order_df['last_updated_date'] = sales_order_df['last_updated'].dt.date
    sales_order_df['last_updated_time'] = sales_order_df['last_updated'].dt.time
    sales_order_df.drop('created_at', axis=1, inplace=True)
    sales_order_df.drop('last_updated', axis=1, inplace=True)
    sales_order_df['agreed_delivery_date'] = pd.to_datetime(sales_order_df['agreed_delivery_date']).dt.date
    sales_order_df['agreed_payment_date'] = pd.to_datetime(sales_order_df['agreed_payment_date']).dt.date
    # sales_order_df['agreed_delivery_date'] = pd.to_datetime(sales_order_df['agreed_delivery_date'], format='%Y-%m-%d').dt.date
    # sales_order_df['agreed_payment_date'] = pd.to_datetime(sales_order_df['agreed_payment_date'], format='%Y-%m-%d').dt.date

    return sales_order_df.reindex(columns=[
        'sales_record_id',
        'sales_order_id',
        'created_date',
        'created_time',
        'last_updated_date',
        'last_updated_time',
        'staff_id',
        'counterparty_id',
        'units_sold',
        'unit_price',
        'currency_id',
        'design_id',
        'agreed_payment_date',
        'agreed_delivery_date',
        'agreed_delivery_location_id'
    ]
    ).rename(columns={'staff_id' : 'sales_staff_id'})

# utilities

# def update_forex_rates():
#     '''Gets forex rates data, writes to file, and updates at approx 8am each day'''
#     forex_log_path = './other_data/forex_rates_log.json'
    
#     now = datetime.now()

#     try:
#         if os.path.exists(forex_log_path):
#             with open(forex_log_path, 'r') as f:
#                 forex = json.loads(f.read())
#                 last_check = datetime.utcfromtimestamp(forex['last_updated'])

#                 if abs(now.day-last_check.day) == 0 or now.hour < 8 :
#                     print('No need to update forex rates')
#                     return
#     except:
#         print('Could not find/read forex rate log; will get forex rates')
    
#     currency_pairs=[
#         'GBPUSD',
#         'EURGBP',
#         'EURUSD',
#         'USDEUR',
#         'USDGBP',
#     ]
    
#     rates = []
#     # for cp in currency_pairs:
#     #     response =requests.get(f'https://www.freeforexapi.com/api/live?pairs={cp}')
#     #     rate = json.loads(response.text)['rates']
#     #     dict = {cp : rate[cp]['rate'] }
#     #     rates.append(dict)

    with open('./other_data/forex_rates.json', 'w') as f:
        f.write(json.dumps(rates, indent=4))
    
    with open(f'{forex_log_path}', 'w') as f:
        info =   {'last_updated':now.timestamp()}
        f.write(json.dumps(info))
    
    print('Updated forex rates')

def load_data_frame_from_json(table_name):
    return pd.read_json(f'{s3_file_reader(table_name, fetch_log_timestamp())}')

def load_data_frame_from_csv(filepath):
    return pd.read_csv(f'{filepath}')

def write_data_frame_to_parquet(data_frame, file_name):
    response = None
    try:
        parquet_buffer = io.BytesIO()
        data_frame.to_parquet(parquet_buffer, index=False)
        parquet_buffer.seek(0)
        s3 = boto3.client('s3')
        response = s3.put_object(Body=parquet_buffer, Bucket='nc-de-awsome-processed-zone', Key=f'transformation_parquet/{file_name}.parquet')
    except Exception:
        raise WriteError('Unable to write to s3')
    return response['ResponseMetadata']['HTTPStatusCode']

def s3_file_reader(table_name, time_stamp):
    response = None
    client = boto3.client('s3')
    try:

        response = client.get_object(
            Bucket= 'nc-de-awsome-ingestion-zone',
            Key= f'totesys/{time_stamp}/{table_name}.json'
        )
    except Exception:
        raise ReadError('Unable to read JSON from s3 bucket (s3_file_reader)')
    return response['Body'].read().decode()

def fetch_log_timestamp(key='query_log.json'):
    time_query_dict = None
    try:
        client = boto3.client('s3')
        time_query = client.get_object(Bucket= 'nc-de-awsome-ingestion-zone', Key=key)
        time_query_dict = json.loads(time_query['Body'].read().decode())
    except Exception:
        raise ReadError('Unable to read JSON from s3 bucket (fetch_log_timestamp')
    print('I am in fetch_log_timestamp')
    return time_query_dict['last_successful_query']

def get_time_of_query():
    tz = pytz.timezone('Europe/London')
    now = datetime.now(tz).strftime('%y-%m-%d %H:%M:%S')
    print('I am in get_time_of_query')
    return now

def create_log_timestamp(time_of_query):
    obj = {
        "last_successful_query" : time_of_query
        # "Last query" : time_of_query,
    }
    print('I am in create_log_timestamp')
    return obj

def write_json_to_bucket(json, bucket_name, key):
    response = None
    try:
        s3 = boto3.client('s3')
        response = s3.put_object(Body=json.encode("utf-8"), Bucket=bucket_name, Key=key)
    except:
        raise WriteError('Unable to write JSON to S3 bucket')
    return response

# errors

class AwsomeError(Exception):
    pass

class TransformationError(AwsomeError):
    pass

class WriteError(AwsomeError):
    pass

class ReadError(AwsomeError):
    pass
