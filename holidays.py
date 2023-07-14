import datetime
import dateutil.relativedelta

import dates


__all__ = [
    'easter',
]


def easter(year: int = dates.Datetime().year) -> dates.Datetime:
    """
    Function to return the day on which Easter occurs in the given year.
    Algorithm used is the anonymous gregorian algorithm.
    https://en.wikipedia.org/wiki/Date_of_Easter#Anonymous_Gregorian_algorithm

    Parameters
    ----------
    year: int
        The year for which the return Easter day is in.
        default = current year

    Returns
    -------
    core.date:
        date representing Easter Sunday

    """
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    g = (8*b + 13) // 25
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7  # apologies for using "l" but I wanted to be consistent with the wiki reference
    m = (a + 11*h + 19*l) // 433
    n = (h + l - 7*m + 90) // 25  # month
    p = int((h + l - 7*m + 33*n + 19) % 32)  # year

    _tmp_date = datetime.date(year, n, p)
    return dates.Datetime(_tmp_date.year, _tmp_date.month, _tmp_date.day)


def is_holiday(in_date):
    if [in_date.day, in_date.month] in [
        [holiday for holiday in holidays.values()] for holidays in regular_holidays.values()
    ]:
        return True
    # need non-regular holidays to be added
    return False


def get_non_regular_holiday(holiday_name: str, year: int = dates.today().year):
    if holiday_name.title() not in non_regular_holidays.keys():
        try:
            holiday_name = alternate_holiday_names[holiday_name.title()]
        except KeyError:
            raise KeyError('Holiday name not found. Use get_available_holidays() to see supported holidays.')
    holiday = non_regular_holidays[holiday_name.title()]
    func = holiday['function']
    return func(year) + dateutil.relativedelta.relativedelta(**holiday['offset'])


regular_holidays = {
    'Christmas Eve': {'day': 24, 'month': 12},
    'Christmas Day': {'day': 25, 'month': 12},
    'Boxing Day':    {'day': 26, 'month': 12},
    'New Years Eve': {'day': 31, 'month': 12},
    'New Years Day': {'day': 1, 'month': 1},
}

non_regular_holidays = {
    'Easter Thursday':
        {'function': easter, 'offset': {'days': -3}},
    # 'Easter Thursday Orthodox': {'function': easter, 'offset': {'days': 0}},
    'Easter Friday':
        {'function': easter, 'offset': {'days': -2}},
    # 'Easter Friday Orthodox': {'function': easter, 'offset': {'days': 0}},
    'Easter Sunday':
        {'function': easter, 'offset': {'days': 0}},
    # 'Easter Sunday Orthodox': {'function': easter, 'offset': {'days': 0}},
    'Easter Monday':
        {'function': easter, 'offset': {'days': 1}},
    # 'Easter Monday Orthodox': {'function': easter, 'offset': {'days': 0}},
    'Pentecost':
        {'function': easter, 'offset': {'days': 49}},
    'Pentecost Monday':
        {'function': easter, 'offset': {'days': 50}},
    'Ascension':
        {'function': easter, 'offset': {'days': 39}},
}

alternate_holiday_names = {
    'Easter': 'Easter Sunday',
    'Whitsun': 'Pentecost',
    'Pinse': 'Pentecost',
    'Whit Monday': 'Pentecost Monday',
    'Holy Thursday': 'Ascension',
}


def get_available_holidays():
    return list(regular_holidays.keys()) + list(non_regular_holidays.keys()) + list(alternate_holiday_names.keys())
