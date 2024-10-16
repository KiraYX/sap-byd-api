from sap_requests import fetch_all_material_data, convert_odate_to_datetime
import json
from datetime import datetime, timedelta
from rich import print as rich_print  # Import rich's print function
from rich.json import JSON  # Import JSON class from rich

# Test environment
data = fetch_all_material_data(tenant='test')  # Default tenant is 'test', can change to 'prod'
# if data:
#     print(f"Total entries retrieved: {len(data)}")  # Print total number of entries retrieved
# rich_print(JSON.from_data(data))  # Print the JSON using rich

# filter data need to modify

# datetime = convert_odate_to_datetime("/Date(1715846596299)/")
# print(datetime)

# Function to filter data based on a specified number of past hours and store the result
def filter_by_last_hours(hours=24):
    # Load data from material_data.json
    with open('data/material_data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Get the current time and calculate the time `hours` ago
    now = datetime.now()
    past_time = now - timedelta(hours=hours)

    # List to store filtered results
    filtered_results = []

    # Loop through the results and filter based on LastChangeDateTime
    for index, item in enumerate(data):
        last_change_dt = convert_odate_to_datetime(item["LastChangeDateTime"])
        # print(len(filtered_results))

        # Print the index along with item details for debugging purposes
        # print(f"Processing item {index}: {item['InternalID']}") 

        # Check if the LastChangeDateTime is within the specified number of hours
        if last_change_dt >= past_time:
            print(item["InternalID"])
            print(last_change_dt)
            filtered_results.append(item)

    # Prepare the new data structure
    filtered_data = {"d": {"results": filtered_results}}

    # Store the filtered data into latest_updated_material.json
    with open('data/latest_updated_material.json', 'w', encoding='utf-8') as json_file:
        json.dump(filtered_data, json_file, ensure_ascii=False, indent=4)

    print(f"Filtered data stored in 'data/latest_updated_material.json'. Total records: {len(filtered_results)}")

# Example usage
filter_by_last_hours(hours=24)  # You can change `hours` to any number