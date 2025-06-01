import datetime

class DateFormat:
    @classmethod
    def convert_date(cls, date):
        if isinstance(date, datetime.date):
            return date
        if isinstance(date, str):
            return datetime.date.fromisoformat(date)
        return date

    @classmethod
    def convert_datetime(cls, date_time):
        if isinstance(date_time, datetime.datetime):
            return date_time
        if isinstance(date_time, str):
            return datetime.datetime.fromisoformat(date_time)
        return date_time
