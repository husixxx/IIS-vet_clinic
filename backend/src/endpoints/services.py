from datetime import datetime


def is_valid_timestamp(timestamp):
    try:
        datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False
    
def is_valid_date(date_string):
    try:
        # Skontroluje, či je dátum vo formáte YYYY-MM-DD
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False