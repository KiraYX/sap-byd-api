import requests
import json
import os
from requests.exceptions import RequestException
from rich import print as rich_print  # Import rich's print function
from rich.json import JSON  # Import JSON class from rich
from config import SAP_PROD_TENANT_HOSTNAME, SAP_TEST_TENANT_HOSTNAME, ODATA_END_POINT_MATERIAL, SAP_CREDENTIALS

# Function to perform API request with tenant selection
def fetch_material_data(tenant='test'):
    # Determine the tenant hostname
    tenant_hostname = SAP_TEST_TENANT_HOSTNAME if tenant == 'test' else SAP_PROD_TENANT_HOSTNAME

    # Base URL for the API
    API_URL = f"https://{tenant_hostname}/sap/byd/odata/cust/v1/{ODATA_END_POINT_MATERIAL}/MaterialCollection"

    # Request headers
    HEADERS = {
        'x-csrf-token': 'fetch',
        'Authorization': f'{SAP_CREDENTIALS}',  # SAP credentials should be properly handled securely
        'Cookie': 'sap-XSRF_LM6_736=cGAbciVfgAzn2oZijGFFRA%3d%3d20241014023811TsiRPfpMcTi_j_dGcZkZTkRKzLGK3QoyuQiTSdPuI_A%3d; sap-usercontext=sap-language=ZH&sap-client=736'
    }

    # Parameters for the request
    params = {
        "$expand": "",
        "$format": "json",
        "sap-language": "ZH",
        "$inlinecount": "allpages",
        "$select": "InternalID,LastChangeDateTime,ObjectID",
        "$filter": "",
        # "$top": 1
    }

    # Use a session to persist connections
    all_data_material = []  # Initialize a list to hold all retrieved data

    with requests.Session() as session:
        session.headers.update(HEADERS)  # Update session with the headers

        try:
            while True:
                response = session.get(API_URL, params=params)  # Perform GET request
                response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

                # Process the response
                data = response.json()  # Automatically decode JSON response
                # rich_print(JSON.from_data(data))  # Print the JSON using rich

                # Add the results to the all_data list
                results = data.get("d", {}).get("results", [])
                all_data_material.extend(results)  # Merge the new results

                # Check if there is a __next URL to fetch more data
                next_url = data["d"].get("__next")
                print(f"Next URL: {next_url}")  # Print the next URL for debugging
                
                if not next_url:  # No more pages to fetch
                    break
                
                # Update the API_URL to the next URL
                API_URL = next_url  # Update to the next URL for the next iteration

            # Create the 'data' folder if it doesn't exist
            os.makedirs('data', exist_ok=True)

            # Write the JSON data to a file in the 'data' folder
            file_path = os.path.join('data', 'material_data.json')  # Create the file path
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            # Return the combined data after all requests are completed
            return all_data_material

        except RequestException as e:
            print(f"An error occurred: {e}")
            return None  # Return None if an error occurs

# Example usage:
# Test environment
data = fetch_material_data(tenant='test')  # Default tenant is 'test', can change to 'prod'
if data:
    print(f"Total entries retrieved: {len(data)}")  # Print total number of entries retrieved
# rich_print(JSON.from_data(data))  # Print the JSON using rich
