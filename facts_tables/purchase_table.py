from main import load_data_frame_from_json, write_data_frame_to_parquet
import pandas as pd

pd.set_option('display.max_columns', None)

df = pd.DataFrame(pd.date_range('1/1/2021','12/31/2021'), columns=['date'])

def dim_date_table():
    df = pd.DataFrame(pd.date_range('1/1/2010','12/31/2023'), columns=['date'])
    df['date_id'] = df['date']
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.strftime("%A")
    df['month_name'] = df['date'].dt.strftime("%B")
    df['quarter'] = df['date'].dt.quarter

    return df

# print(dim_date_table().head(10))

def create_fact_purchase_order():
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


def create_fact_payment():
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

#write to parquet
fact_purchase_order = create_fact_purchase_order()
fact_payment = create_fact_payment()

write_data_frame_to_parquet(fact_purchase_order, 'fact_purchase_order')
write_data_frame_to_parquet(fact_payment, 'fact_payment')
