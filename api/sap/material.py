import requests
from requests.exceptions import RequestException
from rich import print as rich_print  # Import rich's print function
from helper.string_process import split_material_description
from helper.sap_api_url import construct_sap_odata_url
from conf.config import SAP_CREDENTIALS
from utils.json_handler import load_json_file, write_json_file

def construct_single_material_general_data_url(filter_value):
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
        "filter_value": filter_value
    }

    url = construct_sap_odata_url(params)
    return url

def get_request_headers():
    return {
        'x-csrf-token': 'fetch',
        'Authorization': f'{SAP_CREDENTIALS}',
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

    # Construct the API URL
    api_url = construct_single_material_general_data_url(internal_id)

    # Request headers
    session.headers.update(get_request_headers())

    try:
        response = session.get(api_url)
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
            write_json_file('single_material_data.json', material_data)
        else:
            print("No data retrieved or an error occurred.")
