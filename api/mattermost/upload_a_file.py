import requests
from conf.config import MATTERMOST_API_URL, MATTERMOST_CREDENTIALS, MATTERMOST_CHANNEL_ID
from api.jdy.generic import fetch_jdy_single_data_by_id

def upload_files_to_mattermost(file_info_list, channel_name):
    # Validate that the user key exists in the channel configuration
    if channel_name not in MATTERMOST_CHANNEL_ID:
        raise ValueError(f"User key '{channel_name}' not found in channel configuration.")

    # Get the channel ID
    channel_id = MATTERMOST_CHANNEL_ID[channel_name]

    # Prepare headers for Mattermost API
    url = f"{MATTERMOST_API_URL}/files?channel_id={channel_id}"
    headers = {
        'Authorization': MATTERMOST_CREDENTIALS
    }

    # List to store file IDs
    file_ids = []

    for file_info in file_info_list:
        # Step 1: Download the file from the provided URL (in memory)
        response = requests.get(file_info['url'])
        if response.status_code != 200:
            raise Exception(f"Failed to download the file '{file_info['name']}': {response.status_code}")

        # Step 2: Prepare and send the file upload request to Mattermost
        files = {
            'files': (file_info['name'], response.content, file_info['mime'])  # Directly use the content
        }
        payload = {'channel_id': channel_id}

        response = requests.post(url, headers=headers, data=payload, files=files)

        # Check for successful upload
        if response.status_code != 201:
            raise Exception(f"Failed to upload file '{file_info['name']}': {response.status_code}, Response: {response.text}")

        # Parse and store the file ID from the response
        response_data = response.json()
        file_ids.extend(file_info['id'] for file_info in response_data['file_infos'])

    return file_ids


def extract_file_info(response_data):
    # Extract the 'approval_attachment' list from the response data
    attachments = response_data['data'].get('approval_attachment', [])
    
    # Create a list of dictionaries with relevant file information
    file_info_list = [
        {
            'name': attachment.get('name'),
            'size': attachment.get('size'),
            'mime': attachment.get('mime'),
            'url': attachment.get('url')
        }
        for attachment in attachments
    ]
    
    return file_info_list

if __name__ == "__main__":
    
    from rich import print as rich_print

    # Create a session
    with requests.Session() as session:

        # Within sample data only the 3 IDs are required
        sample_data = {
            "appId":"6687c9f329299bd7d3cdee7b",
            "entryId":"669e10e566602b8371646aca",
            "_id":"672c28d98ce2029f4213476f"
        }
 
        po_data = fetch_jdy_single_data_by_id(sample_data, session)

    file_info = extract_file_info(po_data)
    rich_print(file_info)

    # Example usage:

    file_id = upload_files_to_mattermost(file_info, 'yi_xu')
    print(f"Uploaded file ID: {file_id}")
