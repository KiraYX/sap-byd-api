from sap_requests import fetch_all_material_data
import json

# Test environment
# data = fetch_all_material_data(tenant='test')  # Default tenant is 'test', can change to 'prod'
# if data:
#     print(f"Total entries retrieved: {len(data)}")  # Print total number of entries retrieved
# rich_print(JSON.from_data(data))  # Print the JSON using rich

# filter data need to modify
from datetime import datetime, timedelta

# Function to convert OData /Date(...) format to Python datetime
def convert_odate_to_datetime(odata_date):
    # Extract timestamp from OData format '/Date(1715846596299)/'
    timestamp = int(odata_date.strip('/Date()')) / 1000  # Convert milliseconds to seconds
    return datetime.fromtimestamp(timestamp)

# Function to filter data based on a specified number of past hours and store the result
def filter_by_last_hours(hours=9994):
    # Load data from material_data.json
    with open('data/material_data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Get the current time and calculate the time `hours` ago
    now = datetime.now()
    past_time = now - timedelta(hours=hours)

    # List to store filtered results
    filtered_results = []

    # Loop through the results and filter based on LastChangeDateTime
    for item in data["d"]["results"]:
        last_change_dt = convert_odate_to_datetime(item["LastChangeDateTime"])

        # Check if the LastChangeDateTime is within the specified number of hours
        if last_change_dt >= past_time:
            filtered_results.append(item)

    # Prepare the new data structure
    filtered_data = {"d": {"results": filtered_results}}

    # Store the filtered data into latest_updated_material.json
    with open('data/latest_updated_material.json', 'w', encoding='utf-8') as json_file:
        json.dump(filtered_data, json_file, ensure_ascii=False, indent=4)

    print(f"Filtered data stored in 'data/latest_updated_material.json'. Total records: {len(filtered_results)}")

# Example usage
# filter_by_last_hours(hours=24)  # You can change `hours` to any number