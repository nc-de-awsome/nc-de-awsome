from deploy_load_lambda.load_lambda_handler import *
from deploy_load_lambda.load_lambda_handler import load_data_frame_from_parquet_file
import datetime
import pytest
from moto.core import patch_client
from moto import mock_s3
import os
import json
from unittest.mock import patch


dw_password = os.environ['DW_PASSWORD']
dw_username = os.environ['DW_USERNAME']
dw_database_name = os.environ['DW_DATABASE_NAME'] 
dw_host = os.environ['DW_HOST']
dw_port = os.environ['DW_PORT']
dw_region = os.environ['DW_REGION']

conn = pg8000.native.Connection(
            user=dw_username,
            host =dw_host,
            database = dw_database_name,
            port = dw_port,
            password= dw_password
        )

@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    os.environ['AWS_SECURITY_TOKEN'] = 'test'
    os.environ['AWS_SESSION_TOKEN'] = 'test'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'



def test_load_all_data_frame_from_parquet_file():
    table_names = load_data_frame_from_parquet_file(conn)
        
    assert len(table_names) == 11
    assert 'dim_counterparty' in table_names
    assert 'dim_currency' in table_names
    assert 'dim_date' in table_names
    assert 'dim_design' in table_names
    assert 'dim_location' in table_names
    assert 'dim_payment_type' in table_names
    assert 'dim_staff' in table_names
    assert 'dim_transaction' in table_names
    assert 'fact_sales_order' in table_names
    assert 'fact_purchase_order' in table_names
    assert 'fact_payment' in table_names

