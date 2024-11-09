import requests
from conf.config import SAP_CREDENTIALS
from rich import print as rich_print
from helper.url_generator import construct_sap_odata_url
from helper.string_process import split_material_description
from utils.json_processor import write_json_file
from utils.date_time import get_datetime_offset, format_odata_datatime, read_last_update_datetime, save_current_datetime_to_file

# Construct the SAP OData API URL for fetching materials with a filter
def construct_recent_updated_filter_url():

    last_update_time = read_last_update_datetime()
    print("Last update time:", last_update_time)
    # Shift 8 hours to match UTC time, and add 3 minutes to make a small overlap
    filter_from_time = get_datetime_offset(last_update_time, minutes=3, hours=8, days=0)
    print("Filter from time:", filter_from_time)
    filter_time_odata = format_odata_datatime(filter_from_time)
    params = {
        "odata_service": "mcmaterial",
        "entity_set": "MaterialCollection",
        "select": (
            "MaterialID,"
            "ObjectID,"
            "MaterialDescription,"
            "MaterialDescriptionLanguageCode,"
            "InternalDescription_KUT,"
            "IsObsolete_KUT,"
            "LastChangeDateTime,"
            "BaseMeasureUnitCode,"
            "ProductCategoryInternalID,"
            "ProductCategoryDescription,"
            "ProductCategoryLanguageCode"
        ),
        "expand": "",  # No expand by default
        "filter_property": "LastChangeDateTime",
        "filter_operator": "ge",
        "filter_value": filter_time_odata
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

# Utilize pagination to fetch large data, limit is 1000 entries per page
def process_material_page(session, api_url):
    session.headers.update(get_request_headers())
    response = session.get(api_url)
    response.raise_for_status()
    data = response.json()
    
    # Extract and process material data
    material_list = data.get("d", {}).get("results", [])
    
    processed_materials = []
    for material in material_list:
        processed_material = process_material_description(material)
        if processed_material:
            processed_materials.append(processed_material)
    
    # Check for more pages if the response is paginated
    next_link = data.get("d", {}).get("__next")
    return processed_materials, next_link

# Fetch all material data from SAP ByDesign API that match the filter
# By specify the material ID to filter only one material
def fetch_recent_updated_data(session):
    api_url = construct_recent_updated_filter_url()
    materials_data = []
    next_link = api_url

    while next_link:
        materials_batch, next_link = process_material_page(session, next_link)
        materials_data.extend(materials_batch)

    save_current_datetime_to_file()
    return materials_data

# Main block for testing
if __name__ == "__main__":

    with requests.Session() as session:
        material_data_list = fetch_recent_updated_data(session)
 
        # Print the processed material data
        if material_data_list:
            # Print the filtered material data
            rich_print(material_data_list[0])
            # Only print the count of materials when querying all materials
            print("All materials data count:", len(material_data_list))
            write_json_file('recent_updated_materials_data.json', material_data_list)
        else:
            print("No data retrieved or an error occurred.")