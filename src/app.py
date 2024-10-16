from sap_requests import fetch_all_material_data

# Test environment
data = fetch_all_material_data(tenant='test')  # Default tenant is 'test', can change to 'prod'
if data:
    print(f"Total entries retrieved: {len(data)}")  # Print total number of entries retrieved
# rich_print(JSON.from_data(data))  # Print the JSON using rich
