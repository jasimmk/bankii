import datetime


def to_date(dt: datetime.datetime):
    return dt.strftime('%d-%m-%Y')


def to_float(text: str):
    try:
        return float(str(text).replace(',', ''))
    except ValueError:
        return float(0.)
