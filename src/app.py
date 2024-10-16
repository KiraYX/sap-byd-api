import requests
import json
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
        "$select": "InternalID,LastChangeDateTime",
        "$filter": "",
        "$top": 3
    }

    # Use a session to persist connections
    with requests.Session() as session:
        session.headers.update(HEADERS)  # Update session with the headers

        try:
            response = session.get(API_URL, params=params)  # Perform GET request
            response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

            # Process the response
            data = response.json()  # Automatically decode JSON response
            rich_print(JSON.from_data(data))  # Print the JSON using rich

            return data  # Return the response JSON

        except RequestException as e:
            print(f"An error occurred: {e}")
            return None  # Return None if an error occurs

# Example usage:
# Test environment
data = fetch_material_data(tenant='test')  # Default tenant is 'test', can change to 'prod'
