from deploy_ingestion_lambda.lambda_handler import *
from deploy_ingestion_lambda.lambda_handler import _get_table_column_names, _get_table_values
import datetime
import pytest
from moto.core import patch_client
from moto import mock_s3, mock_secretsmanager
import os
import json
from unittest.mock import patch

totesys_password = os.environ['TOTESYS_PASSWORD']
totesys_username = os.environ['TOTESYS_USERNAME']
totesys_database_name = os.environ['TOTESYS_DATABASE_NAME'] 
totesys_host = os.environ['TOTESYS_HOST']
totesys_port = os.environ['TOTESYS_PORT']
totesys_region = os.environ['TOTESYS_REGION']

conn = pg8000.native.Connection(
            user=totesys_username,
            host =totesys_host,
            database = totesys_database_name,
            port = totesys_port,
            password=totesys_password
        )

@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    os.environ['AWS_SECURITY_TOKEN'] = 'test'
    os.environ['AWS_SESSION_TOKEN'] = 'test'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

def test_get_all_table_names_in_totesys_db():
    table_names = get_all_table_names(conn)

    assert len(table_names) == 11
    assert 'counterparty' in table_names
    assert 'currency' in table_names
    assert 'department' in table_names
    assert 'payment' in table_names
    assert 'transaction' in table_names
    assert 'staff' in table_names
    assert 'sales_order' in table_names
    assert 'address' in table_names
    assert 'purchase_order' in table_names
    assert 'payment_type' in table_names
    assert 'design' in table_names

def test_get_table_column_names_in_totesys_db():
    column_names = _get_table_column_names(conn, 'staff')

    assert len(column_names) == 7
    assert "department_id" in column_names
    assert "email_address" in column_names
    assert "first_name" in column_names
    assert "last_name" in column_names
    assert "last_updated" in column_names
    assert "staff_id" in column_names

def test_get_table_values():
    values = _get_table_values(conn, 'staff')

    test_value = [v for v in values if v[0]==1][0]
    assert test_value == [
        1, 
        'Jeremie', 
        'Franey', 
        2, 
        'jeremie.franey@terrifictotes.com', 
        datetime.datetime(2022, 11, 3, 14, 20, 51, 563000),
        datetime.datetime(2022, 11, 3, 14, 20, 51, 563000)
    ]

def test_create_list_of_dictionaries():
    list_of_dicts = create_list_of_dictionaries(conn, 'staff')
    test_dict = [d for d in list_of_dicts if d['staff_id']==1][0]

    assert test_dict == {
        'staff_id': 1, 
        'first_name': 'Jeremie', 
        'last_name': 'Franey', 
        'department_id': 2, 
        'email_address': 'jeremie.franey@terrifictotes.com', 
        'created_at': datetime.datetime(2022, 11, 3, 14, 20, 51, 563000), 
        'last_updated': datetime.datetime(2022, 11, 3, 14, 20, 51, 563000)
    }

def test_list_of_dictionaries_to_json():
    list_of_dicts = create_list_of_dictionaries(conn, 'staff')
    test_dict = [d for d in list_of_dicts if d['staff_id']==1][0]
    test_json = list_of_dictionaries_to_json(test_dict)

    assert type(test_json) == str

    try:
        json.loads(test_json)
        assert True
    except:
        print('Not valid JSON object')
        assert False

@pytest.fixture(scope='function')
def s3(aws_credentials):
    with mock_s3():
        yield boto3.client('s3')

@mock_s3
def test_write_to_json():
    client = boto3.client('s3')
  
    client.create_bucket(Bucket='s3_bucket')
    json_list = json.dumps([{'name': 'Eze'}, {'name': 'Dan'}])
    with pytest.raises(WriteError):
        response = write_json_to_bucket(json_list, 's3_bucket11', 'staff')
    response = write_json_to_bucket(json_list, 's3_bucket', 'staff')
    assert response['ResponseMetadata']['HTTPStatusCode'] == 200

def test_ingest_failure_raises_IngestionError():
    with patch('deploy_ingestion_lambda.lambda_handler.get_all_table_names', return_value=5):
        with pytest.raises(IngestionError):
            ingest(None, None)

def test_get_table_values_raises_SelectQueryError():
    with pytest.raises(SelectQueryError):
        _get_table_values(None, 'staff')

@pytest.fixture(scope='function')
def secretsmanager(aws_credentials):
    with mock_secretsmanager():
        yield boto3.client('secretsmanager', region_name='us-east-1')

def test_get_secret_from_secretsmanager():
    client = boto3.client('secretsmanager', region_name='us-east-1')
    client.create_secret(Name='test_key', SecretString='secret_value')
    secret = get_secret('test_key')
    assert secret == 'secret_value'

def test_get_secret_raises_error_if_secret_not_found():
    with pytest.raises(DatabaseConnectionError):
        client = boto3.client('secretsmanager', region_name='us-east-1')
        get_secret('secret_not_here')


