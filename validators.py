from datetime import datetime

def point_date_validate(d):
    return datetime.strptime(d, '%d.%m.%Y')

