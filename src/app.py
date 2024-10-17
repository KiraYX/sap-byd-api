from sap_requests import fetch_all_material_data, filter_material_by_last_hours
import json
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


# Example usage
filter_material_by_last_hours(hours=24)  # You can change `hours` to any number