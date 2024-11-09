from datetime import datetime, timedelta
from utils.path_finder import find_project_subfolder
import os

# Save the unix timestamp to a file
def save_current_datetime_to_file(filename="last_update_time.txt"):
    folder_path = find_project_subfolder("sap-byd-api", "conf")
    file_path = os.path.join(folder_path, filename)
    
    # Get the current timestamp as a string
    current_timestamp = str(datetime.now().timestamp())
    
    with open(file_path, "w") as file:
        file.write(current_timestamp)

    print(f"Timestamp saved: {current_timestamp}")

# Read the unix timestamp from a file and convert it to a datetime object
def read_last_update_datetime(filename="last_update_time.txt"):
    folder_path = find_project_subfolder("sap-byd-api", "conf")
    file_path = os.path.join(folder_path, filename)

    try:
        with open(file_path, "r") as file:
            timestamp_str = file.read().strip()
            timestamp = float(timestamp_str)  # Convert the string back to a float
            datetime_object = datetime.fromtimestamp(timestamp)
            print(f"Last update: {datetime_object}")
            return datetime_object  # Convert the timestamp to a datetime object
    except FileNotFoundError:
        print(f"{filename} not found. This might be the first run.")
        return None
    except ValueError:
        print(f"Invalid timestamp format in {filename}.")
        return None


# Format time to match ODATA format
def format_odata_datatime(std_datetime):
    return std_datetime.strftime("datetimeoffset'%Y-%m-%dT%H:%M:%S.%f0Z'")

# Find a past time point to fetch recently updated data entries
def get_datetime_offset(base_time, minutes=0, hours=0, days=0):

    # Calculate the time difference
    time_delta = timedelta(days=days, hours=hours, minutes=minutes)
    # Get past time based on the time delta
    past_time = base_time - time_delta
    # Format to match ODATA format
    return past_time

# Convert the odata timestamp string to a ISO datetime object
def convert_odate_to_datetime(odata_date_str):
    # Check if the input is a string
    if isinstance(odata_date_str, str):
        # Remove the '/Date(' and ')' parts, then convert the remaining string to an integer
        try:
            timestamp = int(odata_date_str.replace('/Date(', '').replace(')/', '')) / 1000  # Convert milliseconds to seconds
            # Return the datetime object
            return datetime.fromtimestamp(timestamp)
        except ValueError:
            # If the conversion fails, return None or raise an error
            print("Error: The provided date string is not in the expected format.")
            return None
    else:
        # If the input is not a string, return None or raise an error
        print("Error: The provided date is not a string.")
        return None

if __name__ == "__main__":
    odata_date = "/Date(1731164589685)/"
    print("Odata date:", odata_date)
    iso_datetime = convert_odate_to_datetime(odata_date)
    print("Datetime object:", iso_datetime)

    current_time = format_odata_datatime(datetime.now())
    print("Current time:", current_time)

    # Test save_last_run_time
    save_current_datetime_to_file()

    last_update = read_last_update_datetime()
    print("Last update:", last_update)

    # Test get_datetime_offset
    last_update = get_datetime_offset(last_update, minutes=1, hours=1, days=1)
    print("Last update:", last_update)

    last_update_odata = format_odata_datatime(last_update)
    print("Last update odata:", last_update_odata)
