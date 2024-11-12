import requests
import json
from conf.config import MATTERMOST_API_URL, MATTERMOST_CREDENTIALS, MATTERMOST_CHANNEL_ID
from rich import print as rich_print

import json
import requests

def create_a_post(message, channel_name="yi_xu", file_ids=None, priority="standard"):
    url = f"{MATTERMOST_API_URL}/posts"
    
    # Ensure file_ids is a list or set it to an empty list if None
    file_ids = file_ids if file_ids else []

    # Prepare metadata with priority if it's set
    metadata = {}
    if priority:
        metadata = {
            "priority": {
                "priority": priority,  # "important" or "urgent"
                "requested_ack": True
            }
        }

    payload = json.dumps({
        "channel_id": MATTERMOST_CHANNEL_ID[channel_name],
        "message": message,
        "file_ids": file_ids,
        "metadata": metadata
    })
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': MATTERMOST_CREDENTIALS
    }

    response = requests.post(url, headers=headers, data=payload)

    # Parse JSON response
    response_data = response.json()

    # Return the 'id' from the response
    return response_data.get('id')  # safely returns None if 'id' doesn't exist


if __name__ == "__main__":
    
    message = "| 等级  | 防护描述                       |\n" \
            "| --- | ---------------------------- |\n" \
            "| 0   | 无防护                        |\n" \
            "| 1   | 滴水，垂直滴落                  |\n" \
            "| 2   | 倾斜15°滴水                   |\n" \
            "| 3   | 喷雾                         |\n" \
            "| 9   | 高温高压水柱                    |"


    response = create_a_post(channel_name="yi_xu", message=message, priority="important")
    print("message id:", response)
