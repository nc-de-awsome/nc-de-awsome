from main import load_data_frame_from_json
import pandas as pd
import requests
import json
import os

def dim_date_table():
    df = pd.DataFrame(pd.date_range('1/1/2010','12/31/2023'), columns=['day'])
    df['date_id'] = df.index + 1
    df['year'] = df['day'].dt.year
    df['month'] = df['day'].dt.month
    df['day_of_week'] = df['day'].dt.day
    df['day_name'] = df['day'].dt.strftime("%A")
    df['month_name'] = df['day'].dt.strftime("%B")
    df['quarter'] = df['day'].dt.quarter

    return df

print(dim_date_table().head(5))

# Data needed from sales_order_df, dim_date, dim_staff, dim_counterparty, dim_currency, dim_design, dim_location
sales_order_df = load_data_frame_from_json('sales_order')

def generate_fact_sales_order(sales_order_df):
    df = pd.DataFrame(data=sales_order_df['sales_order_id'], columns=['sales_order_id'])
    df['sales_record_id'] = df.index + 1

    return df

print(generate_fact_sales_order(sales_order_df).head(5))