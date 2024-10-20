import requests
import json
from conf.config import JDY_API_URL, JDY_CREDENTIALS, JDY_IDENTIFIER
from rich import print as rich_print
from helper.convert_json_for_modify import convert_json_for_modify

# Create single material data
def create_jdy_material_data(material_data):
    # Fetch app_id and entry_id from JDY_IDENTIFIER for 'jdy_material'
    app_info = JDY_IDENTIFIER.get('jdy_material')
    
    if not app_info:
        print(f"Error: 'jdy_material' not found in JDY_IDENTIFIER.")
        return None

    app_id = app_info['app_id']
    entry_id = app_info['entry_id']

    # API URL for creating data
    url = f"{JDY_API_URL}/data/create"

    # Construct the payload
    payload = json.dumps({
        "app_id": app_id,
        "entry_id": entry_id,
        "data": material_data  # Input material data is passed here
    })

    # Headers for the request
    headers = {
        'Authorization': JDY_CREDENTIALS,
        'Content-Type': 'application/json'
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=payload)

    # Check for a successful response and return the result
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == '__main__':
    # Example material data
    material_data = {
        "material_id": "18888888",
        "internal_description": "Freedom Gundam_Zaft_X10A",
        "material_name": "Freedom Gundam",
        "brand": "Zaft",
        "model_number": "X10A",
    }

    # Convert the material data
    converted_material_data = convert_json_for_modify(material_data)

    # Create the material data
    created_data = create_jdy_material_data(converted_material_data)
    print(created_data)


