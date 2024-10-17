from sap_requests import fetch_all_material_data, filter_material_by_last_hours

# Test environment
data = fetch_all_material_data(tenant='test')  # Default tenant is 'test', can change to 'prod'

# Example usage
filter_material_by_last_hours(hours=24)  # You can change `hours` to any number
