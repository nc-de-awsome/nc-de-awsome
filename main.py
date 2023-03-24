import pandas as pd
from datetime import datetime

def generate_dim_staff_table():
    staff_df = load_data_frame_from_json('staff')
    select_from_staff_df = staff_df[
        [
            'staff_id',
            'first_name',
            'last_name',
            'email_address',
            'department_id'
        ]
    ]

    department_df = load_data_frame_from_json('department')
    select_from_department_df = department_df[
        [
            'department_id',
            'department_name',
            'location'
        ]
    ]

    join = select_from_staff_df.join(
        select_from_department_df.set_index('department_id'),
        on = 'department_id'
    )

    dim_staff = join[
        [
            'staff_id',
            'first_name',
            'last_name',
            'department_name',
            'location',
            'email_address'
        ]
    ]
    return dim_staff

def generate_dim_design():
    design_df = load_data_frame_from_json('design')
    dim_design = design_df[
        [
            'design_id',
            'design_name',
            'file_location',
            'file_name'
        ]
    ]
    return dim_design

def generate_dim_location():
    address_df = load_data_frame_from_json('address')
    address_columns = address_df[
        [
            'address_id', 
            'address_line_1', 
            'address_line_2', 
            'district', 
            'city', 
            'postal_code', 
            'country',
            'phone'
        ]
    ]
    
    dim_location = address_columns.rename(
        columns={
            'address_id' : 'location_id'
        }
    )
    return dim_location

def generate_dim_counterparty():
    counterparty_df = load_data_frame_from_json('counterparty')
    address_df = load_data_frame_from_json('address')

    return pd.merge(
        counterparty_df,
        address_df,
        left_on = 'legal_address_id',
        right_on = 'address_id',
    )[
        [
            'counterparty_id',
            'counterparty_legal_name', 
            'address_line_1',
            'address_line_2',
            'district',
            'city',
            'postal_code',
            'country',
            'phone'
        ]
    ].rename(
        columns={
            'address_line_1' : 'counterparty_legal_address_line_1',
            'address_line_2' : 'counterparty_legal_address_line_2',
            'district' : 'counterparty_legal_district',
            'city' : 'counterparty_legal_city',
            'postal_code' :'counterparty_legal_postal_code',
            'country' : 'counterparty_legal_country',
            'phone' : 'counterparty_legal_phone_number'
        }
    )

def generate_dim_date():
    # sales_order.created_at
    sales_order_df = load_data_frame_from_json('sales_order')
    print(sales_order_df)
    sales_timestamps=sales_order_df[['created_at']]
    # sales_timestamps.info()
    # print(sales_timestamps)

    # def create_datetime(timestamp)

    datetimes = [pd.to_datetime(pd.Timestamp(s[0]).to_pydatetime().replace(microsecond=0)) for s in sales_timestamps.values]
    dicts = []
    for date in datetimes:
        dicts.append(
                {
                    'date_id' : date.strftime('%y-%m-%d %H:%M:%S'),
                    'year' : date.year,
                    'month' : date.month,
                    'day' : date.day,
                    'day_of_week' : date.day_of_week,
                    'day_name' : date.day_name(),
                    'month_name' : date.month_name(),
                    'quarter' : date.quarter
            }
        )
    
    # x = datetimes[0].strftime('%y-%m-%d %H:%M:%S')
    
    return pd.DataFrame.from_records(dicts)
 
# utilities

def load_data_frame_from_json(table_name):
    return pd.read_json(f'./totesys_json/{table_name}.json')

def write_data_frame_to_parquet(data_frame, file_name):
    data_frame.to_parquet(f'./transformation_parquet/{file_name}.parquet', engine='auto', compression=None, index=False)

    ######### temp code #########
    with open(f'./transformation_parquet/{file_name}.txt', 'w') as f:
        f.write(data_frame.to_string())
    ########### end ############

# run

# dim_staff = generate_dim_staff_table()
# dim_design = generate_dim_design()
# dim_location = generate_dim_location()
# dim_counterparty = generate_dim_counterparty()
dim_date = generate_dim_date()

# write_data_frame_to_parquet(dim_staff, 'dim_staff')
# write_data_frame_to_parquet(dim_design, 'dim_design')
# write_data_frame_to_parquet(dim_location, 'dim_location')
# write_data_frame_to_parquet(dim_counterparty, 'dim_counterparty')
write_data_frame_to_parquet(dim_date, 'dim_date')