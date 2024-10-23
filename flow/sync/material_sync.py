from utils.json_processor import load_json_file
from api.jdy.material import fetch_jdy_material_by_sap_id
from rich import print as rich_print
import requests
from helper.convert_json_sap_to_jdy import convert_sap_response_to_widget_format
from api.jdy.create_material import create_jdy_material_data    
from api.jdy.update_material import update_jdy_material_data

# Main block for standalone execution or future usage as a module
def sync_recently_updated_materials(data_to_sync):
    # Make a session
    rich_print("Data to sync:", data_to_sync)

    data_for_edit = convert_sap_response_to_widget_format(data_to_sync)
    rich_print("Data for edit", data_for_edit)

    with requests.Session() as session:
        for index, item in enumerate(data_to_sync):
            # Print current loop index
            rich_print("item", item)
            current_material_id = item['MaterialID']
            print("Current material id: ", current_material_id)
            current_material = fetch_jdy_material_by_sap_id(current_material_id, session)
            rich_print("Current material:", current_material)
            is_current_found = current_material['data']
            print("is current found in jdy: ", is_current_found)
            # Update the material data if exists
            if is_current_found:
                print("Updating material data...")
                update_jdy = update_jdy_material_data(data_for_edit[index], current_material_id)
                rich_print(update_jdy)
            else:
                print("Material data not found. Creating a new material.")
                rich_print("Right before create:", data_for_edit[index])
                create_jdy = create_jdy_material_data(data_for_edit[index])
                rich_print("Response for new created:", create_jdy)

if __name__ == "__main__":
    # Load data from JSON file
    data_to_sync = load_json_file('recent_updated_materials_data.json')
    rich_print("Loaded json", data_to_sync)
    sync_recently_updated_materials(data_to_sync)