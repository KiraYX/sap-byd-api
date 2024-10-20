import requests
import json
from conf.config import JDY_API_URL, JDY_CREDENTIALS, JDY_IDENTIFIER
from rich import print as rich_print
from helper.convert_json_for_modify import convert_json_for_modify

# Update single material data
def update_jdy_material_data(material_data, data_id):
    # Fetch app_id and entry_id from JDY_IDENTIFIER for 'jdy_material'
    app_info = JDY_IDENTIFIER.get('jdy_material')
    
    if not app_info:
        print(f"Error: 'jdy_material' not found in JDY_IDENTIFIER.")
        return None

    app_id = app_info['app_id']
    entry_id = app_info['entry_id']

    # API URL for creating data
    url = f"{JDY_API_URL}/data/update"

    # Construct the payload
    payload = json.dumps({
        "app_id": app_id,
        "entry_id": entry_id,
        "data_id": data_id,
        "data": material_data  # Input material data is passed here
    })

    rich_print("payload: ", payload)

    # Headers for the request
    headers = {
        'Authorization': JDY_CREDENTIALS,
        'Content-Type': 'application/json'
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=payload)
    rich_print(response.text)

    # Check for a successful response and return the result
    if response.status_code == 200:
        print("response code: ", response.status_code)
        return response.json()
        
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Main function to test
if __name__ == "__main__":
    # Test data
    data_id = "6714b65af07c954f8da5ba79"
    test_data = {
        "internal_description": "Updated Internal Description",
        "material_name": "Gundam",
        "brand": "Anaheim",
        "model_number": "RX78-II",
    }
    test_data = convert_json_for_modify(test_data)
    
    update_jdy_material_data(test_data,data_id)