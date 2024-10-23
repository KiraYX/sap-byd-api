from datetime import datetime, timedelta

# Format time to match ODATA format
def format_odata_datatime(std_datetime):
    return std_datetime.strftime("datetimeoffset'%Y-%m-%dT%H:%M:%S.%f0Z'")

# Find a past time point to fetch recently updated data entries
def get_datetime_offset(minutes=0, hours=0, days=0):

    # Calculate the time difference
    time_delta = timedelta(days=days, hours=hours, minutes=minutes)
    # Get past time based on the time delta
    past_time = datetime.now() - time_delta
    # Format to match ODATA format
    odata_format = format_odata_datatime(past_time)
    return odata_format

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
    odata_date = "/Date(1715846596299)/"
    print("Odata date:", odata_date)
    iso_datetime = convert_odate_to_datetime(odata_date)
    print("Datetime object:", iso_datetime)

    # Test get_datetime_offset
    past_time_str = get_datetime_offset(minutes=30, hours=2, days=1)
    print("Past time:", past_time_str)
