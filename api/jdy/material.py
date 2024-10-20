import requests
import json
from conf.config import JDY_API_URL, JDY_CREDENTIALS, JDY_IDENTIFIER
from rich import print as rich_print

# Find material identifier by material ID (without passing identifier as a parameter)
# Only retrieve one material, return the response
def fetch_jdy_material_by_sap_id(material_id, session, limit=100):
    # Use the JDY_IDENTIFIER from config (assuming we're always using 'jdy_material')
    app_info = JDY_IDENTIFIER.get('jdy_material')

    if not app_info:
        print(f"Error: 'jdy_material' not found in JDY_IDENTIFIER.")
        return None

    app_id = app_info['app_id']
    entry_id = app_info['entry_id']

    url = f"{JDY_API_URL}/data/list"

    # Construct the payload with filters
    payload = {
        "app_id": app_id,  # Use app_id from JDY_IDENTIFIER
        "entry_id": entry_id,  # Use entry_id from JDY_IDENTIFIER
        "fields": [
            "material_id",  # Specify the fields you want to retrieve
            "internal_description",
            # "material_name",
            # "brand",
            # "model_number"
        ],
        "filter": {
            "rel": "and",  # Logical relationship
            "cond": [
                {
                    "field": "material_id",  # Filtering by material_id
                    "type": "text",  # Assuming material_id is text
                    "method": "eq",  # Check for equality
                    "value": [
                        material_id  # Material ID passed as a parameter
                    ]
                }
            ]
        },
        "limit": limit  # Limit for the number of records to retrieve
    }

    headers = {
        'Authorization': f"{JDY_CREDENTIALS}",  # Use your actual API key
        'Content-Type': 'application/json'
    }

    # Make the POST request using the provided session
    response = session.post(url, headers=headers, json=payload)  # Use json parameter instead of data for clarity

    # Check for successful response and return the result
    if response.status_code == 200:
        return response.json()  # Return JSON data if the request was successful
    else:
        print(f"Error: {response.status_code} - {response.text}")  # Print error message if not successful
        return None  # Return None if there was an error



if __name__ == "__main__":
    # Create a session
    with requests.Session() as session:
        # Find material data by material ID
        material_id = "10012345"
        material_data = fetch_jdy_material_by_sap_id(material_id, session)
        rich_print(material_data)