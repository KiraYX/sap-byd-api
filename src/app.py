import json
import os
import requests
from requests.exceptions import RequestException
from rich import print as rich_print  # Import rich's print function
from rich.json import JSON  # Import JSON class from rich
from datetime import datetime, timedelta
from config import SAP_PROD_TENANT_HOSTNAME, SAP_TEST_TENANT_HOSTNAME, ODATA_END_POINT_MATERIAL, SAP_CREDENTIALS, SAP_TENANT_ACTIVE
from text_process import split_material_description, load_json_file
from sap_requests import fetch_all_material_data, fetch_single_material_data, filter_material_by_last_hours
from jdy_requests import create_jdy_material_data, update_jdy_material_data, get_jdy_single_data, find_jdy_material_by_sap_id

# fetch_all_material_data()
material = load_json_file('material_data.json')
# print(material)
sample_material = material[0]
rich_print(sample_material)

internal_id = sample_material['InternalID']
print(internal_id)

jdy_material = find_jdy_material_by_sap_id(internal_id)
rich_print(jdy_material)

update_jdy_material_data(jdy_material, 1)
