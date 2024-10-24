from utils.json_processor import load_json_file
from api.jdy.material import fetch_jdy_material_by_sap_id
from rich import print as rich_print
import requests
from api.jdy.create_material import create_jdy_material_data    
from api.jdy.update_material import update_jdy_material_data
from helper.json_converter import batch_convert_material_sap_to_jdy, batch_convert_jdy_json_to_widget_format

# Main block for standalone execution or future usage as a module
def sync_recently_updated_materials(data_to_sync, debug=False):
    # Make a session
    if debug:
        rich_print("Data to sync:", data_to_sync[0])

    data_jdy_format = batch_convert_material_sap_to_jdy(data_to_sync, debug=False)
    data_for_edit = batch_convert_jdy_json_to_widget_format(data_jdy_format, debug=False)

    if debug:
        rich_print("Data for edit", data_for_edit[0])

    if debug:
        rich_print("Data for edit", data_for_edit[0])

    with requests.Session() as session:
        for index, item in enumerate(data_to_sync):

            # Print current loop index
            print("Current index: ", index)

            if debug:
                rich_print("item", item)

            current_material_id = item['MaterialID']

            print("Current material id: ", current_material_id)

            current_material = fetch_jdy_material_by_sap_id(current_material_id, session)

            if debug:
                rich_print("Current material:", current_material)

            is_current_found = current_material['data']

            if debug:
                print("is current found in jdy: ", is_current_found)

            current_jdy_id = current_material['data'][0]['_id']

            # Update the material data if exists
            if is_current_found:
                print("Updating material data...")
                update_jdy = update_jdy_material_data(material_data=data_for_edit[index], data_id=current_jdy_id, debug=False)
                # if debug:
                rich_print(update_jdy)
            else:
                print("Material data not found. Creating a new material.")
                if debug:
                    rich_print("Right before create:", data_for_edit[index])
                create_jdy = create_jdy_material_data(data_for_edit[index])
                if debug:
                    rich_print("Response for new created:", create_jdy)

if __name__ == "__main__":
    # Load data from JSON file
    data_to_sync = load_json_file('recent_updated_materials_data.json')
    rich_print("Loaded json", data_to_sync[0])
    sync_recently_updated_materials(data_to_sync, debug=False)