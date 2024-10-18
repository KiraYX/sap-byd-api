from jdy_requests import find_jdy_material_by_sap_id
from rich import print as rich_print
from sap_requests import fetch_all_material_data
import json
from text_process import split_material_description, load_json_file


# Fetch all material data from the JSON file
material = load_json_file('material_data.json')

length = len(material)
print(length)

# # The key you're looking for
# target_key = '10009258'

# # Method 2: Using list comprehension
# indexes = [i for i, item in enumerate(material) if item['InternalID'] == target_key]

# if indexes:
#     print(f"Index of {target_key}: {indexes[0]}")  # Get the first match
# else:
#     print(f"{target_key} not found in material data.")