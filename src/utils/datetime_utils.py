from datetime import datetime, timedelta

import numpy
import pytz
from common.constants.datetime_constant import WeekDay
from core.settings.base import TIME_ZONE
from dateutil import parser


def date_string_to_datetime(date_string: str):
    return parser.parse(date_string).date()


def datetime_to_string(date_datetime):
    return str(date_datetime)


def get_weekday_from_date(date_string: str):
    return date_string_to_datetime(date_string).strftime("%A")


def get_current_datetime(timezone=TIME_ZONE, datetime_format="%d/%m/%Y %H:%M:%S"):
    return datetime.now(pytz.timezone(timezone)).strftime(datetime_format)


def get_current_date(timezone=TIME_ZONE):
    return datetime.now(pytz.timezone(timezone)).date()


def number_of_days_between(from_date: str, to_date: str, is_except_weekend: bool):
    if is_except_weekend:
        if get_weekday_from_date(to_date) == WeekDay.MONDAY:
            return numpy.busday_count(from_date, to_date) + 1
        else:
            return numpy.busday_count(from_date, to_date)
    else:
        """
        Get number of days between 2 milestones
        """
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
        to_date = datetime.strptime(to_date, "%Y-%m-%d")
        return abs((to_date - from_date).days) + 1


def minus_date(date_string: str, minus_number: int):
    return datetime_to_string(
        date_string_to_datetime(date_string) - timedelta(days=minus_number)
    )


def plus_date(date_string: str, plus_number: int):
    return datetime_to_string(
        date_string_to_datetime(date_string) + timedelta(days=plus_number)
    )


def extract_duration_to_list_of_dates(
    from_date: str, to_date: str, week_day_remove=None
):
    dates_list = []
    quantity = number_of_days_between(from_date, to_date, is_except_weekend=False)

    if week_day_remove is None:
        for count in range(0, quantity):
            dates_list.append(plus_date(date_string=from_date, plus_number=count))
        return dates_list

    elif len(week_day_remove) > 0:
        for count in range(0, quantity):
            next_date = plus_date(date_string=from_date, plus_number=count)

            if get_weekday_from_date(next_date) not in week_day_remove:
                dates_list.append(next_date)
        return dates_list
