import requests
from conf.config import JDY_API_URL, JDY_CREDENTIALS
from rich import print as rich_print

# Use jiandaoyun app, entry and data ids to get single data with all fields
def get_jdy_single_data(input_data, session):

    # Construct the payload from the input data
    payload = {
        "app_id": input_data.get('appId'),  # Extract app_id from input data
        "entry_id": input_data.get('entryId'),  # Extract entry_id from input data
        "data_id": input_data.get('_id')  # Extract data_id from input data
    }

    url = f"{JDY_API_URL}/data/get"  # Construct the URL
    headers = {
        'Authorization': JDY_CREDENTIALS,  # Use the API credentials
        'Content-Type': 'application/json'
    }

    # Make the POST request using the provided session
    response = session.post(url, headers=headers, json=payload)  # Use json parameter instead of data for clarity

    # Check for successful response
    if response.status_code == 200:
        return response.json()  # Return JSON data if the request was successful
    else:
        print(f"Error: {response.status_code} - {response.text}")  # Print error message if not successful
        return None  # Return None if there was an error
    
if __name__ == "__main__":
    # Create a session
    with requests.Session() as session:
        sample_data = {
            'material_id': '10012345',
            'internal_description': '快换接头_SMC_KQ2H08-G02A',
            '_id': '6683e2b3f99e5bc64e8b6fa3',
            'appId': '6683c4a2399857dff128b206',
            'entryId': '6683c4b0ae4fd18278021f46'
        }
 
        material_data = get_jdy_single_data(sample_data, session)
        rich_print(material_data)