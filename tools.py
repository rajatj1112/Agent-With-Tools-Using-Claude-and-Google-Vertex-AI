from datetime import datetime, timedelta

def add_duration_to_datetime(
    datetime_str, duration=0, unit="days", input_format="%Y-%m-%d"
):
    """
    Adds a specified duration to a datetime string and returns the resulting datetime.
    
    Supports multiple time units with special handling for months and years accounting
    for varying month lengths and leap years.
    
    Args:
        datetime_str (str): The input datetime string to be modified.
        duration (int, optional): The amount of time to add (can be negative for past dates).
                                 Defaults to 0.
        unit (str, optional): The unit of time for the duration. Must be one of:
                             'seconds', 'minutes', 'hours', 'days', 'weeks', 'months', 'years'.
                             Defaults to 'days'.
        input_format (str, optional): Python strptime format string for parsing the input datetime.
                                     Defaults to '%Y-%m-%d'.
    
    Returns:
        str: The resulting datetime formatted as 'Day, Month DD, YYYY HH:MM:SS AM/PM'
             (e.g., 'Thursday, April 03, 2025 10:30:00 AM')
    
    Raises:
        ValueError: If the unit is not one of the supported values.
    """
    date = datetime.strptime(datetime_str, input_format)

    if unit == "seconds":
        new_date = date + timedelta(seconds=duration)
    elif unit == "minutes":
        new_date = date + timedelta(minutes=duration)
    elif unit == "hours":
        new_date = date + timedelta(hours=duration)
    elif unit == "days":
        new_date = date + timedelta(days=duration)
    elif unit == "weeks":
        new_date = date + timedelta(weeks=duration)
    elif unit == "months":
        month = date.month + duration
        year = date.year + month // 12
        month = month % 12
        if month == 0:
            month = 12
            year -= 1
        day = min(
            date.day,
            [
                31,
                29
                if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
                else 28,
                31,
                30,
                31,
                30,
                31,
                31,
                30,
                31,
                30,
                31,
            ][month - 1],
        )
        new_date = date.replace(year=year, month=month, day=day)
    elif unit == "years":
        new_date = date.replace(year=date.year + duration)
    else:
        raise ValueError(f"Unsupported time unit: {unit}")

    return new_date.strftime("%A, %B %d, %Y %I:%M:%S %p")


def set_reminder(content, timestamp):
    """
    Creates and displays a reminder notification.
    
    Currently prints the reminder to console. In a production system, this would
    persist the reminder and send notifications at the specified time.
    
    Args:
        content (str): The message text to display in the reminder notification.
        timestamp (str): The date and time when the reminder should trigger.
                        Should be in ISO 8601 format (YYYY-MM-DDTHH:MM:SS) or Unix timestamp.
    
    Returns:
        None: Prints the reminder information to console.
    """
    print(
        f"----\nSetting the following reminder for {timestamp}:\n{content}\n----"
    )
    
    
def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    """
    Retrieves the current date and time in the specified format.
    
    Args:
        date_format (str, optional): Python strftime format string for the output.
                                    Defaults to '%Y-%m-%d %H:%M:%S'.
    
    Returns:
        str: The current datetime formatted according to the specified format.
    
    Raises:
        ValueError: If date_format is an empty string.
    """
    if not date_format:
        raise ValueError("Date format cannot be empty")
    return datetime.now().strftime(date_format)