from datetime import datetime

def calculate_days(start_date, end_date):
    try:
        d1 = datetime.strptime(start_date, '%Y-%m-%d')
        d2 = datetime.strptime(end_date, '%Y-%m-%d')
        return (d2 - d1).days + 1
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")
    except Exception as e:
        raise Exception(f"Error calculating days: {e}")
