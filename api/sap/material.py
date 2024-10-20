import requests
from requests.exceptions import RequestException
from rich import print as rich_print
from helper.string_process import split_material_description
from helper.sap_api_url import construct_sap_odata_url
from conf.config import SAP_CREDENTIALS
from utils.json_handler import load_json_file, write_json_file

# Construct the SAP OData API URL for fetching materials with a filter
def construct_materials_filter_url(filter_value):
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
        "expand": "",  # No expand by default
        "filter_property": "InternalID",
        "filter_operator": "eq",
        "filter_value": filter_value
    }
    return construct_sap_odata_url(params)

# Generate request headers
def get_request_headers():
    return {
        'x-csrf-token': 'fetch',
        'Authorization': f'{SAP_CREDENTIALS}',
    }

# Split the material description and add new fields
def process_material_description(material_data):
    if not material_data:
        return None

    internal_description = material_data.get('InternalDescription_KUT', '')
    material_name, brand, model_number = split_material_description(internal_description)
    
    # Add the new fields to the material data
    material_data['MaterialName'] = material_name
    material_data['Brand'] = brand
    material_data['ModelNumber'] = model_number
    
    return material_data

# Fetch all material data from SAP ByDesign API that match the filter
# Leave the filter value empty to fetch all materials
def fetch_material_data_by_interal_id(session, internal_id):
    api_url = construct_materials_filter_url(internal_id)
    materials_data = []

    # Update session headers
    session.headers.update(get_request_headers())

    try:
        response = session.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        # Extract material data for the first page
        material_list = data.get("d", {}).get("results", [])
        
        # Process the material data for the first page
        for material in material_list:
            processed_material = process_material_description(material)
            if processed_material:
                materials_data.append(processed_material)

        # Check for more pages if the response is paginated
        next_link = data.get("d", {}).get("__next")
        print("Initial Next link:", next_link)
        while next_link:
            response = session.get(next_link)
            response.raise_for_status()
            data = response.json()
            material_list = data.get("d", {}).get("results", [])
            for material in material_list:
                processed_material = process_material_description(material)
                if processed_material:
                    materials_data.append(processed_material)
            next_link = data.get("d", {}).get("__next")

        return materials_data

    except RequestException as e:
        print(f"An error occurred while fetching material data: {e}")
        return []

# Main block for testing
if __name__ == "__main__":
    material_test = "10013456"  # Replace with the actual internal ID or filter value

    with requests.Session() as session:
        material_data_list = fetch_material_data_by_interal_id(session, material_test)

        # Print the processed material data
        if material_data_list:
            rich_print(material_data_list)
            print("All materials data count:", len(material_data_list))
            write_json_file('all_materials_data.json', material_data_list)
        else:
            print("No data retrieved or an error occurred.")