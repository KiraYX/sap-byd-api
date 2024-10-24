import requests
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from conf.config import MATTERMOST_API_URL, MATTERMOST_CREDENTIALS, MATTERMOST_CHANNEL_ID
from rich import print as rich_print

# Set the headers for the request
headers = {
    'Authorization': MATTERMOST_CREDENTIALS
}

# Directory for storing last post IDs for different channels
last_post_id_dir = 'channel_last_post_ids'

# Ensure the directory exists
if not os.path.exists(last_post_id_dir):
    os.makedirs(last_post_id_dir)

# Function to load the last post ID from a file for a given channel
def load_last_post_id(channel_name):
    file_path = os.path.join(last_post_id_dir, f"{channel_name}_last_post_id.txt")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            last_post_id = file.read().strip()
            if last_post_id:
                return last_post_id
    return None  # Return None if the file doesn't exist or is empty

# Function to save the last post ID to a file for a given channel
def save_last_post_id(channel_name, post_id):
    file_path = os.path.join(last_post_id_dir, f"{channel_name}_last_post_id.txt")
    with open(file_path, 'w') as file:
        file.write(post_id)

# Function to fetch new posts for a given channel name
def fetch_new_posts_for_channel(channel_name):
    # Get the channel ID from the config based on the channel name
    if channel_name not in MATTERMOST_CHANNEL_ID:
        print(f"Channel '{channel_name}' not found in configuration.")
        return
    
    channel_id = MATTERMOST_CHANNEL_ID[channel_name]
    url = f"{MATTERMOST_API_URL}/channels/{channel_id}/posts"

    # Load the last post ID for this channel
    last_post_id = load_last_post_id(channel_name)

    # Set up the query parameters
    params = {}
    if last_post_id:
        params['after'] = last_post_id

    # Make the GET request to fetch the latest posts
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        # Parse the JSON response
        posts_data = response.json()

        # Display the fetched posts
        rich_print(posts_data)

        # Update the last post ID to the most recent post's ID
        if posts_data['order']:  # Check if there are new posts
            latest_post_id = posts_data['order'][0]  # The first post in 'order' is the latest
            save_last_post_id(channel_name, latest_post_id)  # Save the latest post ID
        else:
            print("No new posts found.")
    else:
        print(f"Failed to fetch posts. Status code: {response.status_code}")

# Function to start the polling job
def start_polling(channel_name, interval):
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_new_posts_for_channel, 'interval', seconds=interval, args=[channel_name])
    scheduler.start()
    print(f"Started polling '{channel_name}' every {interval} seconds.")
    return scheduler

# Main block for testing the module
if __name__ == "__main__":
    channel_name = 'yi_xu'  # Replace with your channel name
    polling_interval = 5  # Set the polling interval in seconds
    scheduler = start_polling(channel_name, polling_interval)

    try:
        # Keep the script running to allow the scheduler to run
        while True:
            time.sleep(1)  # Just keep the main thread alive
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # Shutdown the scheduler on exit
        print("Polling stopped.")
