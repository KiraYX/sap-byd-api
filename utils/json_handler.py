from utils import find_project_subfolder
from rich import print as rich_print
import os
import json

# Load data from a specified JSON file
def load_json_file(file_name):
    # Get the path to the JSON file in the 'json' folder
    json_folder_path = find_project_subfolder('sap-byd-api', 'json')
    json_file_path = os.path.join(json_folder_path, file_name)
    with open(json_file_path) as file:
        data = json.load(file)
    return data

# Write data to a specified JSON file
def write_json_file(file_name, data):
    """Write data to a specified JSON file."""
    # Get the path to the JSON file in the 'json' folder
    json_folder_path = find_project_subfolder('sap-byd-api', 'json')
    json_file_path = os.path.join(json_folder_path, file_name)
    
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)  # Use indent for pretty-printing

if __name__ == '__main__':
    test_data = load_json_file('material_data.json')

    # Limit to 2 items
    preview_data = test_data[:2]

    # Print the preview
    rich_print(preview_data)

    # Write the preview to a new JSON file
    write_json_file('material_data_preview.json', preview_data)