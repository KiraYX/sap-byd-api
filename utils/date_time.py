from datetime import datetime, timedelta

def get_datetime_offset(minutes=0, hours=0, days=0):
    """
    获取当前时间减去指定时间的时间点，并格式化为 OData datetimeoffset 字符串。

    :param minutes: 要减去的分钟数，默认为 0。
    :param hours: 要减去的小时数，默认为 0。
    :param days: 要减去的天数，默认为 0。
    :return: 格式化的 OData datetimeoffset 字符串。
    """
    # 计算时间差
    time_delta = timedelta(days=days, hours=hours, minutes=minutes)
    # 获取当前时间减去指定的时间差
    past_time = datetime.now() - time_delta
    # 格式化为 OData 所需的 datetimeoffset 字符串
    odata_format = past_time.strftime("datetimeoffset'%Y-%m-%dT%H:%M:%S.%f'Z")
    return odata_format

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
    print("1 day 2 hours 30 minutes ago:", past_time_str)
