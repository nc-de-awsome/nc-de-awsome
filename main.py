import pandas as pd
import requests
import json
import os
from datetime import datetime


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
    update_forex_rates()

    # transform data into fact and dim tables
    dim_staff = generate_dim_staff(staff_df, department_df)
    dim_design = generate_dim_design(design_df)
    dim_location = generate_dim_location(address_df)
    dim_counterparty = generate_dim_counterparty(counterparty_df, address_df)
    dim_date = generate_dim_date(sales_order_df)
    dim_currency = generate_dim_currency(currency_df, currency_name_df)
    dim_payment = generate_dim_payment_type(payment_df, transaction_df)
    dim_transaction = generate_dim_transaction(transaction_df)

    # writeout fact/dim tables to parquet to load bucket
    write_data_frame_to_parquet(dim_staff, 'dim_staff')
    write_data_frame_to_parquet(dim_design, 'dim_design')
    write_data_frame_to_parquet(dim_location, 'dim_location')
    write_data_frame_to_parquet(dim_counterparty, 'dim_counterparty')
    write_data_frame_to_parquet(dim_date, 'dim_date')
    write_data_frame_to_parquet(dim_currency, 'dim_currency')
    write_data_frame_to_parquet(dim_payment, 'dim_payment')
    write_data_frame_to_parquet(dim_transaction, 'dim_transaction')

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
                    'date_id' : date.strftime('%y-%m-%d %H:%M:%S'),
                    'year' : date.year,
                    'month' : date.month,
                    'day' : date.day,
                    'day_of_week' : date.day_of_week,
                    'day_name' : date.day_name(),
                    'month_name' : date.month_name(),
                    'quarter' : date.quarter
            }
        )
    
    return pd.DataFrame.from_records(dicts)

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
    return pd.read_json(f'./totesys_json/{table_name}.json')

def load_data_frame_from_csv(filepath):
    return pd.read_csv(f'{filepath}')

def write_data_frame_to_parquet(data_frame, file_name):
    data_frame.to_parquet(
        f'./transformation_parquet/{file_name}.parquet', 
        engine='auto', 
        compression=None, 
        index=False
    )
##################### temp code #####################
    write_data_frame_to_local_txt(data_frame, file_name)

##################### temp code #####################
def write_data_frame_to_local_txt(data_frame, file_name):
    with open(f'./transformation_parquet/{file_name}.txt', 'w') as f:
        f.write(data_frame.to_string())

transform(None, None)