import json

def get_all_table_names(conn):
    '''Returns a list of table_name strings of each table in Totesys database
    
        parameters:
            conn: pg8000.native.Connection
        
        returns:
            list of strings 
    '''
    tables = conn.run("SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema='public';")
    table_names = [table[0] for table in tables]
    return table_names

def get_table_column_names(conn, table_name):
    '''Returns a list of column_name strings in table_name

        parameters:
            conn: pg8000.native.Connection
            table_name: string
        
        returns:
            list of strings 
    '''
    columns = conn.run(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema='public';")
    column_names = [column_name[0] for column_name in columns]
    return column_names

def get_table_values(conn, table_name):
    '''Returns a list of lists of values in table_name
    
        parameters:
            conn: pg8000.native.Connection
            table_name: string
        
        returns:
            list of strings 
    '''
    values = conn.run(f'SELECT * FROM {table_name};')
    return values

def create_list_of_dictionaries(conn, table_name):
    '''Returns a list of dicts of column/value pairs from table_name
    
        parameters:
            conn: pg8000.native.Connection
            table_name: string
        
        returns:
            list of dicts 

    '''
    columns = get_table_column_names(conn, table_name)
    values = get_table_values(conn, table_name)
    
    column_value_pairs = []

    for v in values:
        dict = {}
        for i in range(len(columns)):
            dict[columns[i]] = v[i]
        
        column_value_pairs.append(dict)

    return column_value_pairs

def list_of_dictionaries_to_json(list_of_dicts):
    '''Returns a (JSON) string from a list of dicts
        
        parameters:
            list_of_dicts: list of dicts

        returns:
            JSON (string)
    '''
    return json.dumps(list_of_dicts, indent=4, default=str)


