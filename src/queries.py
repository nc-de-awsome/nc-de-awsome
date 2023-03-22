# def get_staff_data(conn):
#     table = 'staff'
#     for row in conn.run(f"SELECT * FROM {table};"):
#         print(row)

def get_all_table_names(conn):
    tables = conn.run("SELECT table_name FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema='public';")

    table_names = [table[0] for table in tables]
    return table_names

def get_table_data(conn, table_name):
    column_names = conn.run(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' AND table_schema='public';")
    values = conn.run(f'SELECT * FROM {table_name};')
    print(column_names)


''' Choose to select from one of the totesys table:
    address, counterparty, currency, department,
    design, payment, payment_type, purchase_order,
    sales_order, staff, or transaction '''

