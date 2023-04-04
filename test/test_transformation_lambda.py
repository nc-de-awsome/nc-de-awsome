from unittest.mock import patch
from deploy_processed_lambda.lambda_handler import *
import pandas as pd
from datetime import datetime

def load_data_frame_from_local_json(table_name):
    return pd.read_json(f'./test/mock_json_data/{table_name}.json')

def test_generate_dim_design():
    design_df = load_data_frame_from_local_json('design')
    actual = generate_dim_design(design_df)

    expected = pd.DataFrame(
                [
            {
                "design_id": 8,
                "design_name": "Wooden",
                "file_location": "/usr",
                "file_name": "wooden-20220717-npgz.json"
            },
            {
                "design_id": 51,
                "design_name": "Bronze",
                "file_location": "/private",
                 "file_name": "bronze-20221024-4dds.json"
            },
            {
                "design_id": 50,
                "design_name": "Granite",
                "file_location": "/private/var",
                "file_name": "granite-20220205-3vfw.json"
            }
        ]
    )
    
    pd.testing.assert_frame_equal(actual, expected)

def test_generate_dim_staff():
    pass
    staff_df = load_data_frame_from_local_json('staff')
    department_df = load_data_frame_from_local_json('department')

    actual = generate_dim_staff(staff_df, department_df)

    expected = pd.DataFrame(
            [
                {
                    "staff_id": 1,
                    "first_name": "Jeremie",
                    "last_name": "Franey",
                    "department_name": "Purchasing",
                    "location": "Manchester",
                    "email_address": "jeremie.franey@terrifictotes.com"
                },
                {
                    "staff_id": 2,
                    "first_name": "Deron",
                    "last_name": "Beier",
                    "department_name": "Production",
                    "location": "Leeds",
                    "email_address": "deron.beier@terrifictotes.com"
                },
                {
                    "staff_id": 3,
                    "first_name": "Jeanette",
                    "last_name": "Erdman",
                    "department_name": "Sales",
                    "location": "Manchester",
                    "email_address": "jeanette.erdman@terrifictotes.com"
                }
            ]
        )

    pd.testing.assert_frame_equal(actual,expected)

def test_generate_dim_location():
    pass
    expected = pd.DataFrame(
        [
            {
                "location_id": 1,
                "address_line_1": "6826 Herzog Via",
                "address_line_2": 'x',
                "district": "Avon",
                "city": "New Patienceburgh",
                "postal_code": "28441",
                "country": "Turkey",
                "phone": "1803 637401"
            },
            {
                "location_id": 2,
                "address_line_1": "179 Alexie Cliffs",
                "address_line_2": 'x',
                "district": 'x',
                "city": "Aliso Viejo",
                "postal_code": "99305-7380",
                "country": "San Marino",
                "phone": "9621 880720"
            },
            {
                "location_id": 3,
                "address_line_1": "148 Sincere Fort",
                "address_line_2": 'x',
                "district": 'x',
                "city": "Lake Charles",
                "postal_code": "89360",
                "country": "Samoa",
                "phone": "0730 783349"
            }
        ]
    )

    address_df = load_data_frame_from_local_json('address')
    actual = generate_dim_location(address_df)

    pd.testing.assert_frame_equal(actual, expected)
    
def test_generate_dim_counterparty():
    counterparty_df = load_data_frame_from_local_json('counterparty')
    address_df = load_data_frame_from_local_json('address')

    actual = generate_dim_counterparty(counterparty_df, address_df)

    expected = pd.DataFrame(
            [
        {
                "counterparty_id": 1,
                "counterparty_legal_name": "Fahey and Sons",
                "counterparty_legal_address_line_1": "6826 Herzog Via",
                "counterparty_legal_address_line_2": "x",
                "counterparty_legal_district": "Avon",
                "counterparty_legal_city": "New Patienceburgh",
                "counterparty_legal_postal_code": "28441",
                "counterparty_legal_country": "Turkey",
                "counterparty_legal_phone_number": "1803 637401",
            
            },
            {
                "counterparty_id": 2,
                "counterparty_legal_name": "Leannon, Predovic and Morar",
                "counterparty_legal_address_line_1": "179 Alexie Cliffs",
                "counterparty_legal_address_line_2": "x",
                "counterparty_legal_district": "x",
                "counterparty_legal_city": "Aliso Viejo",
                "counterparty_legal_postal_code": "99305-7380",
                "counterparty_legal_country": "San Marino",
                "counterparty_legal_phone_number": "9621 880720",
            },
            {
                "counterparty_id": 3,
                "counterparty_legal_name": "Armstrong Inc",
                "counterparty_legal_address_line_1": "148 Sincere Fort",
                "counterparty_legal_address_line_2": "x",
                "counterparty_legal_district": "x",
                "counterparty_legal_city": "Lake Charles",
                "counterparty_legal_postal_code": "89360",
                "counterparty_legal_country": "Samoa",
                "counterparty_legal_phone_number": "0730 783349",
            }
            ]
    )

    pd.testing.assert_frame_equal(actual, expected)

def test_generate_currency():
    currency_df = load_data_frame_from_local_json('currency')

    currency_name_df = pd.DataFrame(
        [
            {
                "CurrencyCode" : "GBP",
                "CurrencyName" : "British Pound Sterling"
            },
            {
                "CurrencyCode" : "USD",
                "CurrencyName" : "US Dollar"
            },
            {
                "CurrencyCode" : "EUR",
                "CurrencyName" : "Euro"
            }
        ]
    )

    actual = generate_dim_currency(currency_df, currency_name_df)
    expected = pd.DataFrame([
        {
            "currency_id" : 1,
            "currency_code" : "GBP",
            "currency_name" : "British Pound Sterling"
        },
        {
            "currency_id" : 2,
            "currency_code" : "USD",
            "currency_name" : "US Dollar"
        },
        {
            "currency_id" : 3,
            "currency_code" : "EUR",
            "currency_name" : "Euro"
        }

        ]
    )
    pd.testing.assert_frame_equal(actual, expected)

def test_generate_dim_payment_type():
    payment_type_df = load_data_frame_from_local_json('payment_type')

    actual = generate_dim_payment_type(payment_type_df)

    expected = pd.DataFrame(
        [
            {
                "payment_type_id": 1,
                "payment_type_name": "SALES_RECEIPT"
            },
            {
                "payment_type_id": 2,
                "payment_type_name": "SALES_REFUND"
            },
            {
                "payment_type_id": 3,
                "payment_type_name": "PURCHASE_PAYMENT"
            },
            {
                "payment_type_id": 4,
                "payment_type_name": "PURCHASE_REFUND"
            }

        ]
    )

    pd.testing.assert_frame_equal(actual, expected)

def test_generate_dim_date():
    sales_df = load_data_frame_from_local_json('sales_order')
    actual = generate_dim_date()
    
    expected = pd.DataFrame(
        [
            {
                "date_id": pd.Timestamp('2022-11-03 14:20:52.187000').to_pydatetime().date(),
                "year" : 2022,
                "month" : 11,
                "day" : 3,
                "day_of_week": 3,
                "day_name" : 'Thursday',
                "month_name": 'November',
                "quarter" : 4
            }
        ]
    )

    pd.testing.assert_frame_equal(actual, expected)

def test_generate_dim_transaction():
    transaction_df = load_data_frame_from_local_json('transaction')
    actual = generate_dim_transaction(transaction_df)
    expected =pd.DataFrame(
        [
            {
                "transaction_id": 1,
                "transaction_type": "PURCHASE",
                "sales_order_id": 0,
                "purchase_order_id": 2,
            },
            {
                "transaction_id": 2,
                "transaction_type": "PURCHASE",
                "sales_order_id": 0,
                "purchase_order_id": 3,
            },
            {
                "transaction_id": 3,
                "transaction_type": "SALE",
                "sales_order_id": 1,
                "purchase_order_id": 0,
            }
    ]
    ).astype(
        {
            'transaction_id': 'int64',
            'transaction_type': 'object',
            'sales_order_id': 'int64',
            'purchase_order_id': 'int64'
        }
    )

    pd.testing.assert_frame_equal(actual,expected)

def test_generate_fact_sales_order():
    sales_order_df = load_data_frame_from_local_json('sales_order')
    actual = generate_fact_sales_order(sales_order_df)
    expected = pd.DataFrame(
        [
        {
            "sales_record_id" : 1,
            "sales_order_id": 1,
            "created_date": pd.Timestamp('2022-11-03 00:00:00').to_pydatetime().date(),
            "created_time": pd.Timestamp('2022-11-03 14:20:52.186000').to_pydatetime().time(),
            "last_updated_date": pd.Timestamp("2022-11-03 14:20:52.186000").to_pydatetime().date(),
            "last_updated_time": pd.Timestamp("2022-11-03 14:20:52.186000").to_pydatetime().time(),
            "sales_staff_id": 16,
            "counterparty_id": 18,
            "units_sold": 84754,
            "unit_price": 2.43,
            "currency_id": 3,
            "design_id": 9,
            "agreed_payment_date": pd.Timestamp("2022-11-03").to_pydatetime().date(),
            "agreed_delivery_date": pd.Timestamp("2022-11-10").to_pydatetime().date(),
            "agreed_delivery_location_id": 4
        },
        {
            "sales_record_id" : 2,
            "sales_order_id": 2,
            "created_date": pd.Timestamp('2022-11-03 14:20:52.186000').to_pydatetime().date(),
            "created_time": pd.Timestamp('2022-11-03 14:20:52.186000').to_pydatetime().time(),
            "last_updated_date": pd.Timestamp("2022-11-03 14:20:52.186000").to_pydatetime().date(),
            "last_updated_time": pd.Timestamp("2022-11-03 14:20:52.186000").to_pydatetime().time(),
            "sales_staff_id": 19,
            "counterparty_id": 8,
            "units_sold": 42972,
            "unit_price": 3.94,
            "currency_id": 2,
            "design_id": 3,
            "agreed_delivery_date": pd.Timestamp("2022-11-07").to_pydatetime().date(),
            "agreed_payment_date": pd.Timestamp("2022-11-08").to_pydatetime().date(),
            "agreed_delivery_location_id": 8
        },
        {
            "sales_record_id": 3,
            "sales_order_id" : 3,
            "created_date": pd.Timestamp('2022-11-03 00:00:00').to_pydatetime().date(),
            "created_time": pd.Timestamp('2022-11-03 14:20:52.186000').to_pydatetime().time(),
            "last_updated_date": pd.Timestamp("2022-11-03 14:20:52.188000").to_pydatetime().date(),
            "last_updated_time": pd.Timestamp("2022-11-03 14:20:52.188000").to_pydatetime().time(),        
            "sales_staff_id": 10,
            "counterparty_id": 4,
            "units_sold": 65839,
            "unit_price": 2.91,
            "currency_id": 3,
            "design_id": 4,
            "agreed_delivery_date": pd.Timestamp("2022-11-06").to_pydatetime().date(),
            "agreed_payment_date": pd.Timestamp("2022-11-07").to_pydatetime().date(),
            "agreed_delivery_location_id": 19
        }
    ]
    )

    pd.testing.assert_frame_equal(actual, expected)

def test_generate_fact_purchase_order():
    purchase_order_df = load_data_frame_from_local_json('purchase_order')
    actual = generate_fact_purchase_order(purchase_order_df)
    expected = pd.DataFrame(
        [
            {
                "purchase_record_id" : 1,
                "purchase_order_id" : 1,
                "created_date" : pd.Timestamp('2022-11-03 14:20:52.000001').to_pydatetime().date(),
                "created_time" : pd.Timestamp('2022-11-03 14:20:52.000001').to_pydatetime().time(),
                "last_updated_date" : pd.Timestamp('2022-11-03 14:20:52.000001').to_pydatetime().date(),
                "last_updated_time" : pd.Timestamp('2022-11-03 14:20:52.000001').to_pydatetime().time(),
                "staff_id" : 12,
                "counterparty_id" : 11,
                "item_code" : "ZDOI5EA",
                "item_quantity" : 371,
                "item_unit_price" : 361.39,
                "currency_id" :2,
                "agreed_delivery_date" : pd.Timestamp('2022-11-09 00:00:00.000001').to_pydatetime().date(),
                "agreed_payment_date" :pd.Timestamp('2022-11-07 00:00:00.000001').to_pydatetime().date(),
                "agreed_delivery_location_id" : 6
            },
            {
                "purchase_record_id" : 2,
                "purchase_order_id" : 2,
                "created_date" : pd.Timestamp('2022-11-03 14:20:52.186000').to_pydatetime().date(),
                "created_time" : pd.Timestamp('2022-11-03 14:20:52.186000').to_pydatetime().time(),
                "last_updated_date" : pd.Timestamp('2022-11-03 14:20:52.186000').to_pydatetime().date(),
                "last_updated_time" : pd.Timestamp('2022-11-03 14:20:52.186000').to_pydatetime().time(),
                "staff_id" : 20,
                "counterparty_id" : 17,
                "item_code" : "QLZLEXR",
                "item_quantity" : 286,
                "item_unit_price" : 199.04,
                "currency_id" :  2,
                "agreed_delivery_date" : pd.Timestamp('2022-11-04 00:20:52.187000').to_pydatetime().date(),
                "agreed_payment_date" :  pd.Timestamp('2022-11-07 14:20:52.187000').to_pydatetime().date(),
                "agreed_delivery_location_id" : 8
            },
            {
                "purchase_record_id" : 3,
                "purchase_order_id" : 3,
                "created_date" : pd.Timestamp('2022-11-03 14:20:52.187000').to_pydatetime().date(),
                "created_time" : pd.Timestamp('2022-11-03 14:20:52.187000').to_pydatetime().time(),
                "last_updated_date" : pd.Timestamp('2022-11-03 14:20:52.187000').to_pydatetime().date(),
                "last_updated_time" : pd.Timestamp('2022-11-03 14:20:52.187000').to_pydatetime().time(),
                "staff_id" : 12,
                "counterparty_id" : 15,
                "item_code" : "AN3D85L",
                "item_quantity" : 839,
                "item_unit_price" : 658.58,
                "currency_id" : 2,
                "agreed_delivery_date" : pd.Timestamp('2022-11-05 00:00:00.187000').to_pydatetime().date(),
                "agreed_payment_date" : pd.Timestamp('2022-11-04 00:00:00.187000').to_pydatetime().date(),
                "agreed_delivery_location_id" : 16
            }
        ]
    )

    pd.testing.assert_frame_equal(actual, expected)

def test_generate_fact_payment():
    payment_df = load_data_frame_from_local_json('payment')
    actual = generate_fact_payment(payment_df)

    expected = pd.DataFrame(
        [
            {
                "payment_record_id":1,
                "payment_id": 2,
                "created_date": pd.Timestamp('2022-11-03 14:20:52.187000').to_pydatetime().date(),
                "created_time": pd.Timestamp('2022-11-03 14:20:52.187000').to_pydatetime().time(),       
                "last_updated_date": pd.Timestamp('2022-11-03 14:20:52.187000').to_pydatetime().date(),
                "last_updated_time": pd.Timestamp('2022-11-03 14:20:52.187000').to_pydatetime().time(),
                "transaction_id": 2,
                "counterparty_id": 15,
                "payment_amount": 552548.62,
                "currency_id": 2,
                "payment_type_id": 3,
                "paid": False,
                "payment_date": pd.Timestamp('2022-11-04 00:00:00').to_pydatetime().date()     
            },
            {
                "payment_record_id":2,
                "payment_id": 3,
                "created_date": pd.Timestamp('2022-11-03 14:20:52.186000').to_pydatetime().date(),
                "created_time": pd.Timestamp('2022-11-03 14:20:52.186000').to_pydatetime().time(),
                "last_updated_date": pd.Timestamp('2022-11-03 14:20:52.186000').to_pydatetime().date(),
                "last_updated_time": pd.Timestamp('2022-11-03 14:20:52.186000').to_pydatetime().time(),
                "transaction_id": 3,
                "counterparty_id": 18,
                "payment_amount": 205952.22,
                "currency_id": 3,
                "payment_type_id": 1,
                "paid": False,
                "payment_date": pd.Timestamp('2022-11-03 00:00:00').to_pydatetime().date() 
            },
            {
                "payment_record_id":3,
                "payment_id": 5,
                "created_date": pd.Timestamp('2022-11-03 14:20:52.187000').to_pydatetime().date(),
                "created_time": pd.Timestamp('2022-11-03 14:20:52.187000').to_pydatetime().time(),
                "last_updated_date": pd.Timestamp('2022-11-03 14:20:52.187000').to_pydatetime().date(),
                "last_updated_time": pd.Timestamp('2022-11-03 14:20:52.187000').to_pydatetime().time(),
                "transaction_id": 5,
                "counterparty_id": 17,
                "payment_amount": 57067.20,
                "currency_id": 2,
                "payment_type_id": 3,
                "paid": False,
                "payment_date": pd.Timestamp('2022-11-06 00:00:00').to_pydatetime().date()  
            }
        ]
    )

    pd.testing.assert_frame_equal(actual, expected)
