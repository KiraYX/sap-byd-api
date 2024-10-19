import requests
from requests.exceptions import RequestException
from rich import print as rich_print  # Import rich's print function
from rich.json import JSON  # Import JSON class from rich
from helper import split_material_description
from conf.config import ODATA_END_POINT_MATERIAL, SAP_CREDENTIALS
from helper import get_tenant_hostname

# Odata request to fetch one material by SAP ID
def fetch_single_material_data(interal_id):

    # Decide the tenant that fetch from
    tenant_hostname = get_tenant_hostname()

    # Select the fields to fetch
    select = (
        "InternalID,"
        "ObjectID,"
        "Description,"
        "InternalDescription_KUT"
    )

    # Filter by Internal ID
    filter = f"InternalID eq '{interal_id}'"

    # Query parameters
    query = f"{ODATA_END_POINT_MATERIAL}/MaterialCollection?$select={select}&$filter={filter}&$format=json"

    # API URL
    API_URL = f"https://{tenant_hostname}/sap/byd/odata/cust/v1/{query}"

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

            return data  # Return the complete data including the new fields

        except RequestException as e:
            print(f"An error occurred: {e}")
            return None  # Return None if an error occurs
        

if __name__ == "__main__":
    # Example usage
    material_data = fetch_single_material_data("10000001")
    print(material_data)