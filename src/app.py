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

# fetch_all_material_data()



