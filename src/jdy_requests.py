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

    # Check for a successful response and return the result
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

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
    url = f"{JDY_URL}/data/create"

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

# Use jiandaoyun app, entry and data ids to get single data with all feilds
def get_jdy_single_data(input_data):

    # Construct the payload from the input data
    payload = {
        "app_id": input_data.get('appId'),  # Extract app_id from input data
        "entry_id": input_data.get('entryId'),  # Extract entry_id from input data
        "data_id": input_data.get('_id')  # Extract data_id from input data
    }

    url = f"{JDY_URL}/data/get"  # Construct the URL
    headers = {
        'Authorization': JDY_CREDENTIALS,  # Use the API credentials
        'Content-Type': 'application/json'
    }

    # Convert payload to JSON string
    payload_json = json.dumps(payload)

    # Make the POST request
    response = requests.post(url, headers=headers, data=payload_json)

    # Check for successful response
    if response.status_code == 200:
        return response.json()  # Return JSON data if the request was successful
    else:
        print(f"Error: {response.status_code} - {response.text}")  # Print error message if not successful
        return None  # Return None if there was an error

# Find material identifier by material ID (without passing identifier as a parameter)
def find_jdy_material_by_sap_id(material_id, limit=100):
    # Use the JDY_IDENTIFIER from config (assuming we're always using 'jdy_material')
    app_info = JDY_IDENTIFIER.get('jdy_material')

    if not app_info:
        print(f"Error: 'jdy_material' not found in JDY_IDENTIFIER.")
        return None

    app_id = app_info['app_id']
    entry_id = app_info['entry_id']

    url = f"{JDY_URL}/data/list"

    # Construct the payload with filters
    payload = json.dumps({
        "app_id": app_id,  # Use app_id from JDY_IDENTIFIER
        "entry_id": entry_id,  # Use entry_id from JDY_IDENTIFIER
        "fields": [
            "material_id",  # Specify the fields you want to retrieve
            "internal_description",
            "material_name",
            "brand",
            "model_number"
        ],
        "filter": {
            "rel": "and",  # Logical relationship
            "cond": [
                {
                    "field": "material_id",  # Filtering by material_id
                    "type": "number",  # Assuming material_id is a number
                    "method": "eq",  # Check for equality
                    "value": [
                        material_id  # Material ID passed as a parameter
                    ]
                }
            ]
        },
        "limit": limit  # Limit for the number of records to retrieve
    })

    headers = {
        'Authorization': f"{JDY_CREDENTIALS}",  # Use your actual API key
        'Content-Type': 'application/json'
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=payload)

    # Check for successful response and return the result
    if response.status_code == 200:
        return response.json()  # Return JSON data if the request was successful
    else:
        print(f"Error: {response.status_code} - {response.text}")  # Print error message if not successful
        return None  # Return None if there was an error
