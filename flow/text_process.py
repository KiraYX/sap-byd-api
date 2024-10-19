import os
import json
from rich import print as rich_print  # Import rich's print function

# Load and print the JSON data from file
def load_json_file(file_name):
    # Get the path to the JSON file in the 'data' folder
    project_folder = os.path.dirname(os.path.dirname(__file__))  # Go up one directory level from 'src'
    json_file_path = os.path.join(project_folder, 'data', file_name)

    # Load the JSON data from the file
    with open(json_file_path) as file:
        data = json.load(file)

    return data

    # Pretty print the JSON data using rich
    # rich_print(data)
