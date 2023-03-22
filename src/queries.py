def get_staff_data(conn):
    table = 'staff'
    for row in conn.run(f"SELECT * FROM {table};"):
        print(row)



''' Choose to select from one of the totesys table:
    address, counterparty, currency, department,
    design, payment, payment_type, purchase_order,
    sales_order, staff, or transaction '''