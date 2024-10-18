import requests
import json
from config import JDY_URL, JDY_CREDENTIALS, JDY_IDENTIFIER

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
    url = f"{JDY_URL}/data/update"

    # Construct the payload
    payload = json.dumps({
        "app_id": app_id,
        "entry_id": entry_id,
        "data_id": data_id,
        "data": material_data  # Input material data is passed here
    })

    # Headers for the request
    headers = {
        'Authorization': JDY_CREDENTIALS,
        'Content-Type': 'application/json'
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=payload)
    print(response.text)

    # Check for a successful response and return the result
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Main function to test
if __name__ == "__main__":
    # Test data
    data_id = "6710b0fbcc6b0c50222679d3"
    test_data = {
        "internal_description": "Updated Internal Description",
        "material_name": "Updated Material Name",
        "brand": "Updated Brand",
        "model_number": "Updated Model Number",
    }
    
    update_jdy_material_data(test_data,data_id)