from rich import print as rich_print  # Import rich's print function
from conf.config import SAP_PROD_TENANT_HOSTNAME, SAP_TEST_TENANT_HOSTNAME, ODATA_END_POINT_MATERIAL, SAP_CREDENTIALS, SAP_TENANT_ACTIVE
from text_process import load_json_file
from sap_requests import fetch_single_material_data
from api.jdy.create_material import create_jdy_material_data, find_jdy_material_by_sap_id
from helper.convert_json_sap_to_jdy import convert_sap_response_to_widget_format
from api.jdy.update_material import update_jdy_material_data

# Fetch all material data
# fetch_all_material_data()   

# Fetch all material data from the JSON file
material = load_json_file('recent_updated_materials_data.json')

start_index = 0

# Loop through the material list starting from the specified index
for i in range(start_index, len(material)):
    sample_material = material[i]

    # Extract Internal ID
    internal_id = sample_material['InternalID']
    print(internal_id)

    # Find JDY material by SAP ID
    jdy_material = find_jdy_material_by_sap_id(internal_id)

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
