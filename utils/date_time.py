from datetime import datetime

# Function to convert OData /Date(...) format to Python datetime
def convert_odate_to_datetime(odata_date):
    # Extract timestamp from OData format '/Date(1715846596299)/'
    timestamp = int(odata_date.strip('/Date()')) / 1000  # Convert milliseconds to seconds
    return datetime.fromtimestamp(timestamp)

if __name__ == "__main__":
    odata_date = '/Date(1715846596299)/'
    print("Odata date:", odata_date)
    iso_datetime = convert_odate_to_datetime(odata_date)
    print("Datetime object:", iso_datetime)