from src.queries import *
from src.conn import connect_to_database

def test_get_table_names_in_totesys_db():
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