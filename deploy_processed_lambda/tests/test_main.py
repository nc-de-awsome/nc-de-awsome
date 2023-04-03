from deploy_processed_lambda.lambda_handler import *
import pytest
import moto
from moto.core import patch_client
from moto import mock_s3
import os
from unittest.mock import patch
import pandas as pd

@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    os.environ['AWS_SECURITY_TOKEN'] = 'test'
    os.environ['AWS_SESSION_TOKEN'] = 'test'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

@pytest.fixture(scope='function')
def s3(aws_credentials):
    with mock_s3():
        yield boto3.client('s3')

@mock_s3
def test_s3_file_reader():
    s3_client = boto3.client('s3')
    currency_data = json.dumps([
    {
        "currency_id": 1,
        "currency_code": "GBP",
        "created_at": "2022-11-03 14:20:49.962000",
        "last_updated": "2022-11-03 14:20:49.962000"
    },
    {
        "currency_id": 2,
        "currency_code": "USD",
        "created_at": "2022-11-03 14:20:49.962000",
        "last_updated": "2022-11-03 14:20:49.962000"
    },
    {
        "currency_id": 3,
        "currency_code": "EUR",
        "created_at": "2022-11-03 14:20:49.962000",
        "last_updated": "2022-11-03 14:20:49.962000"
    }
])
    s3_client.create_bucket(Bucket='nc-de-awsome-ingestion-zone')
    s3_client.put_object(Body=currency_data, Bucket='nc-de-awsome-ingestion-zone', Key=f'totesys/23-03-28 06:07:23/currency.json')
    response = s3_file_reader('currency','23-03-28 06:07:23')
    assert type(response) == str
    currency_dict = json.loads(response)
    assert len(currency_dict) == 3
    assert 'currency_id' in currency_dict[0]
    assert 'currency_code' in currency_dict[0]
    assert 'created_at' in currency_dict[0]
    assert 'last_updated' in currency_dict[0]


def test_s3_file_reader_errors():
    with patch('deploy_processed_lambda.lambda_handler.s3_file_reader', return_value=5):
        with pytest.raises(ReadError):
            s3_file_reader('currency', '23-03-30 06:07:23')

@mock_s3
def test_fetch_log_timestamp():
    s3_client = boto3.client('s3')
    time_data = json.dumps(
    {
    "last_successful_query": "23-03-29 09:49:05"
    }
)
    s3_client.create_bucket(Bucket='nc-de-awsome-ingestion-zone')
    s3_client.put_object(Body=time_data, Bucket='nc-de-awsome-ingestion-zone', Key=f'query_log.json')

    time_stamp = fetch_log_timestamp()
    assert time_stamp == "23-03-29 09:49:05"

def test_fetch_log_timestamp_errors():
    with patch('deploy_processed_lambda.lambda_handler.fetch_log_timestamp', return_value=5):
        with pytest.raises(ReadError):
            fetch_log_timestamp('not_query_log.json')

@mock_s3
def test_write_data_frame_to_parquet():
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket='nc-de-awsome-processed-zone')
    df = pd.DataFrame([
    {
        "currency_id": 1,
        "currency_code": "GBP",
        "created_at": "2022-11-03 14:20:49.962000",
        "last_updated": "2022-11-03 14:20:49.962000"
    },
    {
        "currency_id": 2,
        "currency_code": "USD",
        "created_at": "2022-11-03 14:20:49.962000",
        "last_updated": "2022-11-03 14:20:49.962000"
    },
    {
        "currency_id": 3,
        "currency_code": "EUR",
        "created_at": "2022-11-03 14:20:49.962000",
        "last_updated": "2022-11-03 14:20:49.962000"
    }
    ])
    response = write_data_frame_to_parquet(df, 'currency')
    assert response == 200
    
def test_write_data_frame_to_parquet():
    df_dict = {
        "currency_id": 3,
        "currency_code": "EUR",
        "created_at": "2022-11-03 14:20:49.962000",
        "last_updated": "2022-11-03 14:20:49.962000"
    }
    with patch('deploy_processed_lambda.lambda_handler.write_data_frame_to_parquet', return_value=5):
        with pytest.raises(WriteError):
            write_data_frame_to_parquet(df_dict, 'currency')

@mock_s3
def test_transform_error():
    with patch('deploy_processed_lambda.lambda_handler.write_data_frame_to_parquet'):
        with pytest.raises(TransformationError):
            transform(None, None)

