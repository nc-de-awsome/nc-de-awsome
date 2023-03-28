from unittest.mock import patch
from deploy_processed_lambda.src.main import load_data_frame_from_json, generate_dim_design
import pandas as pd

# with patch('deploy_ingestion_lambda.src.queries.get_all_table_names', return_value=5):


def load_data_frame_from_local_json(table_name):
    return pd.read_json(f'/Users/roshaka/Desktop/northcoders/data-eng/nc-de-awsome/mock_json_data/{table_name}.json')

def test_load_data_frame_from_json():
    
    with patch(
         'deploy_processed_lambda.src.main.load_data_frame_from_json',
               return_value=load_data_frame_from_local_json('design')
        ):
        design_df = load_data_frame_from_local_json('design')
        dim_design = generate_dim_design(design_df)

    expected = pd.DataFrame(
                [
            {
                "design_id": 8,
                "created_at": "2022-11-03 14:20:49.962000",
                "design_name": "Wooden",
                "file_location": "/usr",
            },
            {
                "design_id": 51,
                "created_at": "2023-01-12 18:50:09.935000",
                "design_name": "Bronze",
                "file_location": "/private",
            },
            {
                "design_id": 50,
                "created_at": "2023-01-12 16:31:09.694000",
                "design_name": "Granite",
                "file_location": "/private/var",
            }
        ]
    )
        
    assert dim_design[['design_id']] ==  expected[['design_id']]
    
def test_hi():
        assert True