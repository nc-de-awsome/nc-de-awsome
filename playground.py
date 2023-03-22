import boto3
import pg8000.native

client = boto3.client('rds')
host = 'nc-data-eng-totesys-production.chpsczt8h1nu.eu-west-2.rds.amazonaws.com'
port = 5432
username = 'project_user_2'
region = 'eu-west-2'
password = 'WiSoz6BeH4a8Mj'
db_name = 'totesys'

#generates AWS token
rds_auth_token = client.generate_db_auth_token(DBHostname=host, Port=port, DBUsername=username, Region=region)

#connects to totesys DB
con =  pg8000.native.Connection(user=username, host=host, database=db_name, port=port, password=password)

''' Choose to select from one of the totesys tables: 
    address, counterparty, currency, department, 
    design, payment, payment_type, purchase_order, 
    sales_order, staff, or transaction '''

table = 'design'
table_extract = con.run(f"SELECT * FROM {table} LIMIT 4;")
columns = con.columns
cols = []
print(f'Selected table contains {con.row_count} rows')

for column in columns:
    cols.append(column['name'])
print(cols)

for row in table_extract:
    print(row)

con.close()


