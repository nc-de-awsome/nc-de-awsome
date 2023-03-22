from src.conn import connect_to_database
from src.queries import *

conn_totesys = connect_to_database('totesys')

# get_staff_data(conn_totesys)

get_all_table_names(conn_totesys)
get_table_data(conn_totesys, 'staff')
conn_totesys.close()
