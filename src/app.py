import json
import os
import requests
from requests.exceptions import RequestException
from rich import print as rich_print  # Import rich's print function
from rich.json import JSON  # Import JSON class from rich
from datetime import datetime, timedelta
from config import SAP_PROD_TENANT_HOSTNAME, SAP_TEST_TENANT_HOSTNAME, ODATA_END_POINT_MATERIAL, SAP_CREDENTIALS, SAP_TENANT_ACTIVE
from text import split_material_description
from sap_requests import fetch_all_material_data, fetch_single_material_data, filter_material_by_last_hours

# Test environment
# data = fetch_all_material_data(tenant='test')  # Default tenant is 'test', can change to 'prod'

# Example usage
# filter_material_by_last_hours(hours=24)  # You can change `hours` to any number

print("tenant", SAP_TENANT_ACTIVE)
# Function to fetch a single material's data by Internal ID

material_data = fetch_single_material_data('10000000')
rich_print(material_data)

