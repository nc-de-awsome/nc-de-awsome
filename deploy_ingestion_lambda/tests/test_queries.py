from deploy_ingestion_lambda.src.queries import *
from deploy_ingestion_lambda.src.conn import connect_to_database
import datetime
import pytest

def test_get_all_table_names_in_totesys_db():
    conn = connect_to_database('totesys')
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
    conn = connect_to_database('totesys')
    column_names = get_table_column_names(conn, 'staff')

    assert len(column_names) == 7
    assert "department_id" in column_names
    assert "email_address" in column_names
    assert "first_name" in column_names
    assert "last_name" in column_names
    assert "last_updated" in column_names
    assert "staff_id" in column_names

def test_get_table_values():
    conn = connect_to_database('totesys')
    values = get_table_values(conn, 'staff')

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
    conn = connect_to_database('totesys')
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
    conn = connect_to_database('totesys')
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