import requests
from io import BytesIO

# File information
file_info = {
    "name": "GZ-PO241532-1107_潼德.pdf",
    "size": 161594,
    "mime": "application/pdf",
    "url": "https://files.jiandaoyun.com/86282628-5d89-4b4b-8fa8-94600feb2c9a?attname=GZ-PO241532-1107_%E6%BD%BC%E5%BE%B7.pdf&e=1732600799&token=bM7UwVPyBBdPaleBZt21SWKzMylqPUpn-05jZlas:vJIrbBHZtKr4nXSNCxrzm50DYSw="
}

# Download the file from Jiandaoyun (in memory)
response = requests.get(file_info['url'])

if response.status_code == 200:
    print("Start to upload the file")
    
    # Store the file in memory using BytesIO
    file_content = BytesIO(response.content)

    # Mattermost API settings
    mattermost_url = "https://mattermost.mujin.com.cn/api/v4/files"
    channel_id = "qapyujpmoigh5jhfr1k7aejg1h"
    token = "8rr35eh9apr3mbzde7kkoq5xqh"

    # Prepare file for upload
    files = {
        'files': (file_info['name'], file_content, file_info['mime']),
    }

    headers = {
        'Authorization': f'Bearer {token}',
    }

    # Step 1: Upload the file to Mattermost
    upload_response = requests.post(mattermost_url, headers=headers, files=files, data={'channel_id': channel_id})

    # Print the response content to debug the structure
    print("Upload Response JSON:")
    print(upload_response.json())  # Debug the response

    # Step 2: Check the response format and extract file ID
    if upload_response.status_code == 201:  # 201 indicates a successful upload
        print("File uploaded successfully")
        
        # Debug: Check the full response
        response_data = upload_response.json()
        print(f"Full upload response: {response_data}")
        
        # Extract the file ID based on the response structur
