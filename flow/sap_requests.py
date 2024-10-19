import os
import json
import requests
from datetime import datetime, timedelta
from requests.exceptions import RequestException
from rich import print as rich_print  # Import rich's print function
from rich.json import JSON  # Import JSON class from rich
from text_process import split_material_description
from conf.config import SAP_PROD_TENANT_HOSTNAME, SAP_TEST_TENANT_HOSTNAME, ODATA_END_POINT_MATERIAL, SAP_CREDENTIALS, SAP_TENANT_ACTIVE

# Decide the tenant by argument or by active tenant
def get_tenant_hostname(tenant=None):
    # If tenant is None, use the current active tenant
    if tenant is None:
        tenant = SAP_TENANT_ACTIVE  # Use the current active tenant

    # Determine the tenant hostname based on the provided tenant
    tenant_hostname = SAP_TEST_TENANT_HOSTNAME if tenant == 'test' else SAP_PROD_TENANT_HOSTNAME
    print(f"Tenant hostname determined: {tenant_hostname}")
    return tenant_hostname

def fetch_single_material_data(interal_id):

    tenant_hostname = get_tenant_hostname()

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
        # print("Session headers updated")

        try:
            # Perform GET request to fetch the single material data
            response = session.get(API_URL)  # No need for params since we're fetching a single item
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
            # print("Request successful")

            # Process the response
            data = response.json()  # Automatically decode JSON response
            # print("Response JSON decoded")

            # Extract the material data from the response
            material_data = data.get("d", {}).get("results", [{}])[0]  # Get the first result

            # Extract InternalDescription_KUT
            internal_description = material_data.get('InternalDescription_KUT', '')

            # Split the description into name, brand, and model number
            material_name, brand, model_number = split_material_description(internal_description)

            # Add the new fields to the material data
            material_data['MaterialName'] = material_name
            material_data['Brand'] = brand
            material_data['ModelNumber'] = model_number

            # Optional: Write the data to a file (if needed)
            # file_path = os.path.join('data', f'material_{interal_id}.json')  # Create a unique file name for the material
            # with open(file_path, 'w', encoding='utf-8') as json_file:
            #     json.dump(data, json_file, ensure_ascii=False, indent=4)  # Write the original data with new fields
            # print(f"Material data written to file: {file_path}")

            return data  # Return the complete data including the new fields

        except RequestException as e:
            print(f"An error occurred: {e}")
            return None  # Return None if an error occurs

# Function to perform API request with tenant selection
def fetch_all_material_data():
    
    # Determine the tenant hostname
    tenant_hostname = get_tenant_hostname()

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
        "$filter": ""
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
                # print(f"Next URL: {next_url}")  # Print the next URL for debugging
                
                if not next_url:  # No more pages to fetch
                    break
                
                # Update the API_URL to the next URL
                API_URL = next_url  # Update to the next URL for the next iteration

            # Create the 'data' folder if it doesn't exist
            # os.makedirs('data', exist_ok=True)

            # Write the JSON data to a file in the 'data' folder
            file_path = os.path.join('data', 'material_data.json')  # Create the file path
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(all_data_material, json_file, ensure_ascii=False, indent=4)

            # Return the combined data after all requests are completed
            return all_data_material

        except RequestException as e:
            print(f"An error occurred: {e}")
            return None  # Return None if an error occurs
        
# Function to convert OData /Date(...) format to Python datetime
def convert_odate_to_datetime(odata_date):
    # Extract timestamp from OData format '/Date(1715846596299)/'
    timestamp = int(odata_date.strip('/Date()')) / 1000  # Convert milliseconds to seconds
    return datetime.fromtimestamp(timestamp)

# Function to filter data based on a specified number of past hours and store the result
def filter_material_by_last_hours(hours=24):
    # Load data from material_data.json
    with open('data/material_data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Get the current time and calculate the time `hours` ago
    now = datetime.now()
    past_time = now - timedelta(hours=hours)

    # List to store filtered results
    filtered_results = []

    # Loop through the results and filter based on LastChangeDateTime
    for index, item in enumerate(data):
        last_change_dt = convert_odate_to_datetime(item["LastChangeDateTime"])
        # print(len(filtered_results))

        # Print the index along with item details for debugging purposes
        # print(f"Processing item {index}: {item['InternalID']}") 

        # Check if the LastChangeDateTime is within the specified number of hours
        if last_change_dt >= past_time:
            print(item["InternalID"])
            print(last_change_dt)
            filtered_results.append(item)

    # Prepare the new data structure
    filtered_data = filtered_results

    # Store the filtered data into latest_updated_material.json
    with open('data/latest_updated_material.json', 'w', encoding='utf-8') as json_file:
        json.dump(filtered_data, json_file, ensure_ascii=False, indent=4)

    print(f"Filtered data stored in 'data/latest_updated_material.json'. Total records: {len(filtered_results)}")
