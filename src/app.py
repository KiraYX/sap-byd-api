import json
import os
import requests
from requests.exceptions import RequestException
from rich import print as rich_print  # Import rich's print function
from rich.json import JSON  # Import JSON class from rich
from datetime import datetime, timedelta
from config import SAP_PROD_TENANT_HOSTNAME, SAP_TEST_TENANT_HOSTNAME, ODATA_END_POINT_MATERIAL, SAP_CREDENTIALS
from text import split_material_description

# Test environment
# data = fetch_all_material_data(tenant='test')  # Default tenant is 'test', can change to 'prod'

# Example usage
# filter_material_by_last_hours(hours=24)  # You can change `hours` to any number


# Function to fetch a single material's data by Internal ID
def fetch_single_material_data(interal_id, tenant='test'):
    print(f"Fetching material data for Internal ID: {interal_id}, Tenant: {tenant}")
    
    # Determine the tenant hostname
    tenant_hostname = SAP_TEST_TENANT_HOSTNAME if tenant == 'test' else SAP_PROD_TENANT_HOSTNAME
    print(f"Tenant hostname determined: {tenant_hostname}")

    # Construct the API URL for fetching a single material
    API_URL = f"https://{tenant_hostname}/sap/byd/odata/cust/v1/{ODATA_END_POINT_MATERIAL}/MaterialCollection?$select=InternalID,ObjectID,Description,InternalDescription_KUT&$filter=InternalID eq '{interal_id}'&$format=json"

    # Request headers
    HEADERS = {
        'x-csrf-token': 'fetch',
        'Authorization': f'{SAP_CREDENTIALS}',
        'Cookie': 'sap-XSRF_LM6_736=cGAbciVfgAzn2oZijGFFRA%3d%3d20241014023811TsiRPfpMcTi_j_dGcZkZTkRKzLGK3QoyuQiTSdPuI_A%3d; sap-usercontext=sap-language=ZH&sap-client=736'
    }

    # Use a session to persist connections
    with requests.Session() as session:
        session.headers.update(HEADERS)  # Update session with the headers
        print("Session headers updated")

        try:
            # Perform GET request to fetch the single material data
            response = session.get(API_URL)  # No need for params since we're fetching a single item
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            print("Request successful")

            # Process the response
            data = response.json()  # Automatically decode JSON response
            print("Response JSON decoded")

            # Extract the material data from the response
            material_data = data.get("d", {}).get("results", [{}])[0]  # Get the first result
            print(f"Material data extracted: {material_data}")

            # Extract InternalDescription_KUT
            internal_description = material_data.get('InternalDescription_KUT', '')

            # Split the description into name, brand, and model number
            material_name, brand, model_number = split_material_description(internal_description)

            # Add the new fields to the material data
            material_data['MaterialName'] = material_name
            material_data['Brand'] = brand
            material_data['ModelNumber'] = model_number

            # Optional: Write the data to a file (if needed)
            file_path = os.path.join('data', f'material_{interal_id}.json')  # Create a unique file name for the material
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)  # Write the original data with new fields
            print(f"Material data written to file: {file_path}")

            return data  # Return the complete data including the new fields

        except RequestException as e:
            print(f"An error occurred: {e}")
            return None  # Return None if an error occurs
        
material_data = fetch_single_material_data('10000000', tenant='test')
rich_print(material_data)

