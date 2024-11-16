from datetime import datetime

"""
Validates the timestamp format (YYYY-MM-DD HH:MM:SS)

Args:
    timestamp (str): The timestamp to validate
"""

def is_valid_timestamp(timestamp):
    try:
        datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

"""
Validates the date format (YYYY-MM-DD)

Args:
    date_string (str): The date to validate
"""
def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False