import datetime
import re
from typing import Dict


regex_days = re.compile(r'(Mo|Tu|We|Th|Fr|Sa|Su)(-|, )?(Mo|Tu|We|Th|Fr|Sa|Su)?')
regex_hours = re.compile(r'\d\d:\d\d-\d\d:\d\d')
regex_date = re.compile(r'(?P<day>Mo|Tu|We|Th|Fr|Sa|Su) (?P<hour>\d\d:\d\d)')
regex_time_slot = re.compile(r'(?P<d1>\d\d:\d\d)-(?P<d2>\d\d:\d\d)')
days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
regex_data_day = re.compile(r'; *')
# regex_time_slot = re.compile(r'(?P<h1>\d\d):(?P<m1>\d\d)-(?P<h2>\d\d):(?P<m2>\d\d)')


class building_opening_hours:
    school = {
        'Mo': ['08:30-11:30', '13:30-16:30'],
        'Tu': ['08:30-11:30', '13:30-16:30'],
        'We': ['08:30-11:30'],
        'Th': ['08:30-11:30', '13:30-16:30'],
        'Fr': ['08:30-11:30', '13:30-16:30'],
        'Sa': [],
        'Su': [],
    }
    college = {
        'Mo': ['08:00-11:30', '13:00-17:30'],
        'Tu': ['08:00-11:30', '13:00-17:30'],
        'We': ['08:00-11:30'],
        'Th': ['08:00-11:30', '13:30-17:30'],
        'Fr': ['08:00-11:30', '13:30-17:30'],
        'Sa': [],
        'Su': [],
    }
    bus_station = {
        'Mo': ['05:00-23:30'],
        'Tu': ['05:00-23:30'],
        'We': ['05:00-23:30'],
        'Th': ['05:00-23:30'],
        'Fr': ['05:00-23:30'],
        'Sa': ['05:00-23:30'],
        'Su': ['05:00-23:30'],
    }
    tram_station = {
        'Mo': ['05:00-24:00'],
        'Tu': ['05:00-24:00'],
        'We': ['05:00-24:00'],
        'Th': ['05:00-24:00'],
        'Fr': ['05:00-24:00'],
        'Sa': ['05:00-24:00'],
        'Su': ['05:00-24:00'],
    }
    childcare = {
        'Mo': ['07:00-19:00'],
        'Tu': ['07:00-19:00'],
        'We': ['07:00-19:00'],
        'Th': ['07:00-19:00'],
        'Fr': ['07:00-19:00'],
        'Sa': [],
        'Su': [],
    }
    residential = {
        'Mo': ['07:00-19:00'],
        'Tu': ['07:00-19:00'],
        'We': ['07:00-19:00'],
        'Th': ['07:00-19:00'],
        'Fr': ['07:00-19:00'],
        'Sa': ['07:00-19:00'],
        'Su': ['07:00-12:00'],
    }


def time_slot_int(time_slot: str) -> tuple:
    """
        time_slot: HH:MM-HH:MM
    """
    time_slot = regex_time_slot.fullmatch(time_slot)
    return hour_int(time_slot.group('d1')), hour_int(time_slot.group('d2'))


def hour_int(hour: str) -> float:
    """
        hour: HH:MM
    """
    h, sep, m = hour.partition(':')
    if not sep:
        raise AttributeError
    return int(h)+int(m)/60


def date_percent_in_week(date: str) -> float:
    """
        date: DD HH:MM
    """
    date = date_check(date)
    date_percent = 100/7 * days.index(date.group('day'))

    nb_hour = int(date.group('hour').partition(':')[0])
    date_percent += 100/7/24 * nb_hour

    return date_percent


def date_check(date: str) -> re.Match:
    """
        date: DD HH:MM
    """
    date = regex_date.fullmatch(date)
    if not date:
        print(f"Paramètre hour incorrect {date}")
        raise AttributeError
    return date


def date_to_int(date: str) -> datetime:
    """
        date: YYYY-MM-DD
    """
    return datetime.datetime(*map(int, date.split('-')))


def now():
    return datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)


class Opening_hours(str):
    @property
    def __dict__(self) -> Dict[str, list]:
        ret = default_opening_hours()
        for opening_days in re.split(regex_data_day, self):
            days_data = regex_days.findall(opening_days)
            hours_data = regex_hours.findall(opening_days)
            if not days_data or not hours_data:
                continue
            for day_beg, sep, day_end in days_data:
                found = False
                for day in ret:
                    if found or day == day_beg:
                        found = True
                        ret[day].extend(hours_data)
                        if not day_end or day == day_end:
                            break

        return ret


def default_opening_hours(string: str = '') -> dict:
    if not string:
        return {
            day: []
            for day in days}

    return {
        day: [string]
        for day in days}
