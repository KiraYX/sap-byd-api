import requests
import json
from config import JDY_URL, JDY_CREDENTIALS, JDY_IDENTIFIER

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
            "material_id"  # Specify the fields you want to retrieve
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
