import datetime
# import json
import pathlib

from typing import Union, List, Optional

import countries
import dates
import holidays


__all__ = [
    'available_elements',
    'available_countries',
    'get',
    'generate_holidays',
    'generate_regular_holidays',
    'generate_non_regular_holidays',
    'is_holiday',
]


def available_elements() -> list:
    return [
        'holidays',
        'currency',
        'capital',
        'exchanges',
    ]


def available_countries():
    return [file.name.removesuffix('.conf') for file in pathlib.Path('./Lib/countries').iterdir()]


def get(
        country: Union[str, List[str]] = None,
        elements: Union[str, List[str]] = None,
        date_interval: List[Union[datetime.date, dates.Datetime]] = None,
) -> str:
    """
    Function used to calculate and return the data elements for the requested countries in the requested date interval

    Parameters
    ----------
    country: Union[str, List[str]] = None
        the countries for which the data should be retrieved for
        default of None returns all available countries
    elements: Union[str, List[str]] = None
        the data elements to be retrieved
        default of None returns all available data elements
    date_interval: List[Union[datetime.date, dates.Datetime]] = None
        the date interval between which the holidays should be returned if holidays is requested as an element
        default of None returns all holidays for the current year and following 4 years, 5 years total

    Returns
    -------
    str: JSON string representing the requested data
    """
    if country is None:
        country = available_countries()
    else:
        country = [country.upper() for country in country] if isinstance(country, list) else [country.upper()]

    if elements is None:
        elements = available_elements()
    else:
        elements = [element.lower() for element in elements] if isinstance(elements, list) else [elements.lower()]

    if date_interval is None:
        start_date = round(dates.Datetime(), 0)
        end_date = dates.Datetime(start_date.year + 5, 12, 31)
        date_interval = [start_date, end_date]
    else:
        # do some type checking if needed
        date_interval = date_interval

    # return_json_dict = dict()

    # return json.dumps(return_json_dict, indent=4)
    return f'{country=}, {elements=}, {date_interval=}'


def generate_regular_holidays(
        country: str,
        date_interval: Optional[List[Union[datetime.date, dates.Datetime]]] = None,
        date_format: str = '%Y-%m-%d'
) -> dict:
    """

    Parameters
    ----------
    country: str
    date_interval
    date_format

    Returns
    -------
    dict of holidays
    """
    if country not in available_countries():
        raise AttributeError(
            f"Country {country} not implemented. For a list of implement countries call available_countries()."
        )

    country = countries.Country(country)
    date_interval = date_interval or [round(dates.today()), dates.today().next_year_end]
    min_date, max_date = min(date_interval), max(date_interval)
    tmp_holiday_dates = dict()

    # Regular Holidays - holidays that fall on the same day each year
    country_regular_holidays = country.conf.get('Holidays').get('Regular Holidays')

    for year in dates.all_ints_between(min_date.year, max_date.year):
        tmp_holiday_dates.update(
            {
                year: {
                    key:
                    str(dates.Datetime([year, values['month'], values['day']], str_format=date_format))
                    for key, values in holidays.regular_holidays.items()
                    if key.lower() in [holiday.lower() for holiday in country_regular_holidays]
                }
            }
        )

    return tmp_holiday_dates


def generate_non_regular_holidays(
        country: str,
        date_interval: Optional[List[Union[datetime.date, dates.Datetime]]] = None,
        date_format: str = '%Y-%m-%d'
) -> dict:
    if country not in available_countries():
        raise AttributeError(
            f"Country {country} not implemented. For a list of implement countries call available_countries()."
        )

    country = countries.Country(country)
    date_interval = date_interval or [round(dates.today()), dates.today().next_year_end]
    min_date, max_date = min(date_interval), max(date_interval)
    tmp_holiday_dates = list()

    # Regular Holidays - holidays that fall on the same day each year
    country_regular_holidays = country.conf.get('Holidays').get('Non Regular Holidays')

    # for year in dates.all_ints_between(min_date.year, max_date.year):
    #     tmp_holiday_dates.append(
    #         [
    #             dates.Datetime([year, values['month'], values['day']])
    #             for key, values in holidays.regular_holidays.items()
    #             if key in country_regular_holidays
    #         ]
    #     )

    return {'holidays': tmp_holiday_dates}


def generate_holidays(
        country: str,
        date_interval: List[Union[datetime.date, dates.Datetime]] = None,
        date_format: str = '%Y-%m-%d'
) -> dict:

    tmp_holiday_dates = generate_regular_holidays(country, date_interval, date_format)
    # tmp_holiday_dates.update(generate_non_regular_holidays(country, date_interval, date_format))

    return {'holidays': tmp_holiday_dates}


def is_holiday(in_date: dates.Datetime, holiday_calendar: Union[str, countries.Country] = None) -> bool:
    if holiday_calendar is None:
        return False
