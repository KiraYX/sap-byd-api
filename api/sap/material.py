import requests
from requests.exceptions import RequestException
from rich import print as rich_print  # Import rich's print function
from helper import split_material_description, construct_sap_odata_url
from conf.config import SAP_CREDENTIALS
from helper import get_tenant_hostname

def construct_sap_api_url():
    params = {
        "odata_service": "mcmaterial",
        "entity_set": "MaterialCollection",
        "select": (
            "InternalID,"
            "ObjectID,"
            "Description,"
            "InternalDescription_KUT,"
            "Obsolete_KUT"
        ),
        "expand": (
            ""
        ),
        "filter_property": "InternalID",
        "filter_operator": "eq",
        "filter_value": "10013000"
    }

    url = construct_sap_odata_url(params)
    return url

def get_request_headers():
    return {
        'x-csrf-token': 'fetch',
        'Authorization': f'{SAP_CREDENTIALS}',
        'Cookie': 'sap-XSRF_LM6_736=cGAbciVfgAzn2oZijGFFRA%3d%3d20241014023811TsiRPfpMcTi_j_dGcZkZTkRKzLGK3QoyuQiTSdPuI_A%3d; sap-usercontext=sap-language=ZH&sap-client=736'
    }

def process_material_data(material_data):
    internal_description = material_data.get('InternalDescription_KUT', '')
    material_name, brand, model_number = split_material_description(internal_description)
    
    # Add the new fields to the material data
    material_data['MaterialName'] = material_name
    material_data['Brand'] = brand
    material_data['ModelNumber'] = model_number
    
    return material_data

def fetch_single_material_data(session, internal_id):
    tenant_hostname = get_tenant_hostname()
    API_URL = construct_sap_api_url()
    session.headers.update(get_request_headers())

    try:
        response = session.get(API_URL)
        response.raise_for_status()
        data = response.json()
        material_data = data.get("d", {}).get("results", [{}])[0]
        return process_material_data(material_data)  # Process material data here

    except RequestException as e:
        print(f"An error occurred: {e}")
        return None  # Return None if an error occurs

# Testing the module
if __name__ == "__main__":
    material_test = "10009999"
    with requests.Session() as session:
        # Replace '10000001' with a valid internal ID for testing
        material_data = fetch_single_material_data(session, material_test)

        # Print the processed material data
        if material_data:
            rich_print(material_data)
        else:
            print("No data retrieved or an error occurred.")
