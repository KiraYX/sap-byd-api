from jdy_requests import find_jdy_material_by_sap_id
from config import JDY_URL, JDY_CREDENTIALS, JDY_IDENTIFIER
from rich import print as rich_print  # Import rich's print function
import requests
import json
    
# Example usage of the function
material_keys = find_jdy_material_by_sap_id(material_id=10000000)

# Print the result
rich_print(material_keys)

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

# Example usage
input_data = material_keys

# Pass the first item from input_data to the function
result = get_jdy_single_data(input_data['data'][0])
rich_print(result)  # Print the result