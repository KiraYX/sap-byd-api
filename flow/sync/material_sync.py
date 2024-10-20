from utils.json_handler import load_json_file
from api.jdy.material import fetch_jdy_material_by_sap_id
from rich import print as rich_print
import requests
from helper.convert_json_for_modify import convert_json_for_modify
from api.jdy.create_material import create_jdy_material_data    
from api.jdy.update_material import update_jdy_material_data

# Main block for standalone execution or future usage as a module
def sync_recently_updated_materials(data_to_sync):
    # Make a session
    with requests.Session() as session:
        for item in data_to_sync:
            # Print current loop index
            current_material = fetch_jdy_material_by_sap_id(item['MaterialID'], session)
            material_raw_data = current_material['data']
            rich_print(material_raw_data)

            # Update the material data if exists
            if material_raw_data:
                print("Updating material data...")
                data_for_edit = convert_json_for_modify(item)
                update_jdy = update_jdy_material_data(data_for_edit, material_raw_data[0]['_id'])
                rich_print(update_jdy)
            else:
                print("Material data not found. Creating a new material.")
                data_for_edit = convert_json_for_modify(item)
                create_jdy = create_jdy_material_data(data_for_edit)
                rich_print(create_jdy)

if __name__ == "__main__":
    # Load data from JSON file
    data_to_sync = load_json_file('recent_updated_materials_data.json')
    sync_recently_updated_materials(data_to_sync)