from jdy_requests import find_jdy_material_by_sap_id, get_jdy_single_data, create_jdy_material_data, update_jdy_material_data
from config import JDY_URL, JDY_CREDENTIALS, JDY_IDENTIFIER, MATERIAL_FIELD_MAPPING
from rich import print as rich_print  # Import rich's print function
import requests
import json
    
# # Example usage of the function
# material_keys = find_jdy_material_by_sap_id(material_id=10000000)

# # Print the result
# rich_print(material_keys)

# # Example usage
# input_data = material_keys['data'][0]

# # Pass the first item from input_data to the function
# result = get_jdy_single_data(input_data)
# rich_print(result)  # Print the result


sample_data_id = "6710b0fbcc6b0c50222679d3"
# Sample material data
sample_material_data = {
    MATERIAL_FIELD_MAPPING["material_id"]: {"value": "123456789"},
    MATERIAL_FIELD_MAPPING["internal_description"]: {"value": "Test value 2"},
    MATERIAL_FIELD_MAPPING["material_name"]: {"value": "Test Name 2"},
    MATERIAL_FIELD_MAPPING["brand"]: {"value": "Test Brand 2"},
    MATERIAL_FIELD_MAPPING["model_number"]: {"value": "Test Model 2"},
}

rich_print(sample_material_data)

result = update_jdy_material_data(sample_material_data, sample_data_id)
rich_print(result)