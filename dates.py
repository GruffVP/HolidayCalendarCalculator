import datetime

from dateutil import parser
from dateutil.relativedelta import relativedelta

from typing import List, Optional, Union


__all__ = [
    'Datetime',

    'is_month_end',
    'is_weekend',
    'is_year_end',
    'now',
    'today',
]


class Datetime(datetime.datetime):
    def __new__(
            cls,
            *date: Union[int, datetime.date, datetime.datetime, List[int]],
            str_format: Optional[str] = None,
            country: Optional[str] = None,
            input_format: Optional[str] = None,
            day_first: bool = True,
    ):
        if len(date) == 1:
            date = date[0]

        if not date:
            date = datetime.datetime.now()
        elif isinstance(date, (tuple, list)):
            date = datetime.datetime(*date)
        elif isinstance(date, datetime.datetime):
            date = date
        elif isinstance(date, datetime.date):
            date = datetime.datetime.combine(date, datetime.datetime.min.time())
        elif input_format is None:
            date = parser.parse(date, dayfirst=day_first)
        else:
            date = datetime.datetime.strptime(input_format)

        self = super().__new__(
            cls, date.year, date.month, date.day, date.hour, date.minute, date.second, date.microsecond
        )
        if str_format is None:
            if date.time() == datetime.datetime.min.time():
                self.str_format = '%Y-%m-%d'
            else:
                self.str_format = '%Y-%m-%d %H:%M:%S'
        else:
            self.str_format = str_format
        self.datetime = date
        self.country = country
        return self

    def __str__(self):
        s = self.strftime(self.str_format)
        return s

    def __add__(self, other):
        if isinstance(other, (datetime.timedelta, relativedelta)):
            return Datetime(self.datetime + other)
        return Datetime(self.datetime + datetime.timedelta(other))

    def __sub__(self, other):
        if isinstance(other, (datetime.timedelta, relativedelta, datetime.date, datetime.datetime)):
            return self.datetime - other
        return self.datetime - datetime.timedelta(other)

    def __round__(self, n=2):
        if n == 0:
            return Datetime(datetime.datetime(self.year, 1, 1), str_format=self.str_format)
        if n == 1:
            return Datetime(datetime.datetime(self.year, self.month, 1), str_format=self.str_format)
        values = self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsecond
        return Datetime(datetime.datetime(*values[0:n+1]), str_format=self.str_format)

    @property
    def week_day(self):
        return self.strftime('%A')

    @property
    def is_weekend(self):
        return is_weekend(self)

    @property
    def is_month_end(self):
        return is_month_end(self)

    @property
    def prev_month_end(self):
        return round(self, 1) - 1

    @property
    def prev_business_month_end(self):
        return round(self, 1).add_bdays(-1, holiday_calendar=self.country)

    @property
    def next_month_end(self):
        return round(self.add_months(1), 1) - 1

    @property
    def next_business_month_end(self):
        return round(self.add_months(1), 1).add_bdays(-1, holiday_calendar=self.country)

    @property
    def is_year_end(self):
        return is_year_end(self)

    @property
    def prev_year_end(self):
        return round(self, 0) - 1

    @property
    def next_year_end(self):
        return round(self.add_years(1), 0) - 1

    def add_days(self, n_days: int):
        return Datetime(self.datetime + datetime.timedelta(n_days))

    def add_months(self, n_months: int):
        return Datetime(self.datetime + relativedelta(months=n_months))

    def add_years(self, n_years: int):
        return Datetime(self.datetime.replace(year=self.datetime.year + n_years))

    def add_bdays(self, n_days: int, holiday_calendar: str = None):
        tmp_date = self.datetime
        if not holiday_calendar:
            while n_days != 0:
                tmp_date = tmp_date + datetime.timedelta(n_days / abs(n_days))
                if not is_weekend(tmp_date) and not is_holiday(tmp_date, holiday_calendar):
                    n_days = n_days - (n_days / abs(n_days))
        return Datetime(tmp_date)


def is_weekend(in_date: Datetime) -> bool:
    return in_date.strftime('%a').upper() in ('SAT', 'SUN')


def is_month_end(in_date: Datetime) -> bool:
    return in_date.month != (in_date + 1).month


def is_year_end(in_date: Datetime) -> bool:
    return in_date.year != (in_date + 1).year


def today():
    return Datetime(datetime.date.today())


def now():
    return Datetime(datetime.datetime.now())


def all_ints_between(int1: int, int2: int):
    max_int, min_int = max(int1, int2), min(int1, int2)

    out_list = [max_int]
    while max_int > min_int:
        max_int -= 1
        out_list.append(max_int)
    return out_list
