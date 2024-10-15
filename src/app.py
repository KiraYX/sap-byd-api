import requests
import json
from requests.exceptions import RequestException
from rich import print as rich_print  # Import rich's print function
from rich.json import JSON  # Import JSON class from rich
from config import HOSTNAME, ODATA_SERVICE_NAME, CREDENTIALS

# Base URL for the API
API_URL = f"https://{HOSTNAME}/sap/byd/odata/cust/v1/{ODATA_SERVICE_NAME}/MaterialCollection"

# Request headers
HEADERS = {
    'x-csrf-token': 'fetch',
    'Authorization': f'Basic {CREDENTIALS}',
    'Cookie': 'sap-XSRF_LM6_736=cGAbciVfgAzn2oZijGFFRA%3d%3d20241014023811TsiRPfpMcTi_j_dGcZkZTkRKzLGK3QoyuQiTSdPuI_A%3d; sap-usercontext=sap-language=ZH&sap-client=736'
}

# Parameters for the request
params = {
    "$expand": "",
    "$format": "json",
    "sap-language": "ZH",
    "$inlinecount": "allpages",
    "$select": "InternalID,LastChangeDateTime",
    "$filter": "",
    "$top": 2
}

# Use a session to persist connections
with requests.Session() as session:
    session.headers.update(HEADERS)  # Use headers from the config

    try:
        response = session.get(API_URL, params=params)  # Use API_URL from the config
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        # Process the response
        data = response.json()  # Automatically decode JSON response
        rich_print(JSON.from_data(data))

        # Count the number of entries in the "results" list
        entries_count = len(data["d"].get("results", []))  # Adjusted to access "results"
        print(f"Number of data entries returned: {entries_count}")  # Print the count

    except RequestException as e:
        print(f"An error occurred: {e}")
