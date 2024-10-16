import json

# Load data from the JSON file
with open('data/material_data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Count entries
entry_count = len(data)
print(f"Total entries in JSON: {entry_count}")
