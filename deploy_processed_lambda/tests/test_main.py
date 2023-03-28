from deploy_processed_lambda.main import *
import pytest
import moto
from moto.core import patch_client
from moto import mock_s3
import os
from unittest.mock import patch

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
    time_query = fetch_log_timestamp()
    print(time_query)
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
    response = s3_file_reader('currency')
    assert type(response) == str
    currency_dict = json.loads(response)
    assert len(currency_dict) == 3
    assert 'currency_id' in currency_dict[0]
    assert 'currency_code' in currency_dict[0]
    assert 'created_at' in currency_dict[0]
    assert 'last_updated' in currency_dict[0]


def test_s3_file_reader_errors():
    with patch('deploy_processed_lambda.main.s3_file_reader', return_value=5):
        with pytest.raises(ReadError):
            s3_file_reader('currency')


# access s3
# read file
# return correct values
# return correct format/filetype
# return corect error message (ReadError)
# s3 file reader reads latest data dump (dynamic date folder names)
