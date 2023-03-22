from src.conn import *
from src.queries import *

conn_totesys = connect_to_database('totesys')

get_staff_data(conn_totesys)
conn_totesys.close()
