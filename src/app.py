import json
import os
import requests
from requests.exceptions import RequestException
from rich import print as rich_print  # Import rich's print function
from rich.json import JSON  # Import JSON class from rich
from datetime import datetime, timedelta
from config import SAP_PROD_TENANT_HOSTNAME, SAP_TEST_TENANT_HOSTNAME, ODATA_END_POINT_MATERIAL, SAP_CREDENTIALS, SAP_TENANT_ACTIVE
from text_process import split_material_description, load_json_file
from sap_requests import fetch_all_material_data, fetch_single_material_data, filter_material_by_last_hours
from jdy_requests import create_jdy_material_data, get_jdy_single_data, find_jdy_material_by_sap_id
from convert_json import convert_json_for_modify
from convert_sap_json_to_jdy import convert_sap_response_to_widget_format
from update_material import update_jdy_material_data

# Fetch all material data
# fetch_all_material_data()   

# Fetch all material data from the JSON file
material = load_json_file('material_data.json')

for item in material:

    # # Take the first material for processing
    sample_material = item
    # rich_print(sample_material)

    # # Extract Internal ID
    internal_id = sample_material['InternalID']
    print(internal_id)

    # Find JDY material by SAP ID
    jdy_material = find_jdy_material_by_sap_id(internal_id)
    # rich_print(jdy_material)

    # Check if JDY material exists
    if jdy_material["data"]:  # JDY material found
        data_id = jdy_material["data"][0]["_id"]
        # print(data_id)

        # Fetch SAP material data
        sap_material = fetch_single_material_data(internal_id)
        # rich_print(sap_material)

        # Convert SAP data to the required format
        sap_data_converted = convert_sap_response_to_widget_format(sap_material)
        # rich_print(sap_data_converted)

        # Update JDY material data
        update_jdy = update_jdy_material_data(sap_data_converted, data_id)
        # print(update_jdy)

    else:  # JDY material not found, create a new one
        print("JDY material not found. Creating a new material.")
        
        # Fetch SAP material data
        sap_material = fetch_single_material_data(internal_id)
        # rich_print(sap_material)

        # Convert SAP data to the required format
        sap_data_converted = convert_sap_response_to_widget_format(sap_material)
        # rich_print(sap_data_converted)

        # Create JDY material data
        create_jdy = create_jdy_material_data(sap_data_converted)
        # print(create_jdy)
