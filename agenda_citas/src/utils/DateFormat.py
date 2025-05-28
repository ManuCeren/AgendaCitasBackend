import datetime

class DateFormat:
    @classmethod
    def convert_date(self, date):
        return datetime.datetime.strftime(date,'%d/%m/%Y')

    @classmethod
    def convert_datetime(cls, date_time):
        if isinstance(date_time, datetime.datetime):
            return date_time.strftime('%d/%m/%Y %H:%M')
        return date_time