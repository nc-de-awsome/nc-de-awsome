from deploy_ingestion_lambda.src.conn import connect_to_database
from deploy_ingestion_lambda.src.queries import *

def ingest():

    conn_totesys = connect_to_database('totesys')

    # get_staff_data(conn_totesys)

    # get_all_table_names(conn_totesys)
    # get_table_column_names(conn_totesys, 'staff')

    dicts = create_list_of_dictionaries(conn_totesys, 'staff')
    print(dicts[0])

    # print(get_table_column_names(conn_totesys, 'staff'))

    conn_totesys.close()
        