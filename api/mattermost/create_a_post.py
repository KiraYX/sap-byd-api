import requests
import json
from conf.config import MATTERMOST_API_URL, MATTERMOST_CREDENTIALS, MATTERMOST_CHANNEL_ID
from rich import print as rich_print

def create_a_post(message, channel_name="yi_xu"):
    url = f"{MATTERMOST_API_URL}/posts"

    payload = json.dumps({
    "channel_id": MATTERMOST_CHANNEL_ID[channel_name],
    "message": message,
    #   "file_ids": [
    #     "fwxqutix1jnst898z3xxpy57pa"
    #   ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': MATTERMOST_CREDENTIALS
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response

if __name__ == "__main__":
    response = create_a_post(channel_name="yi_xu", message="test function")
    rich_print(response.text)
