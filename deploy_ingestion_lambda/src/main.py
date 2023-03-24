from deploy_ingestion_lambda.src.conn import connect_to_database
from deploy_ingestion_lambda.src.queries import *
from deploy_ingestion_lambda.src.errors import IngestionError

def ingest():
    try:
        conn = connect_to_database()
        table_names = get_all_table_names(conn)
        for table in table_names:
            rows = create_list_of_dictionaries(conn, table)
            json = list_of_dictionaries_to_json(rows)
            # write_json_to_bucket(json, 'nc-de-awsome-ingestion-zone', f'totesys/{table}.json' )

            ######### temp code #########
            with open(f'totesys_json/{table}.json', 'w') as f:
                f.write(json)
            ########### end ############

        conn.close()
    except Exception as e:
        raise IngestionError(f'{e}')

ingest()