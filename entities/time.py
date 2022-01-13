import datetime
import re


regex_date = re.compile(r'(?P<day>Mo|Tu|We|Th|Fr|Sa|Su) (?P<hour>\d\d:\d\d)')
regex_time_slot = re.compile(r'(?P<d1>\d\d:\d\d)-(?P<d2>\d\d:\d\d)')


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


def date_check(date: str):
    """
        date: DD HH:MM
    """
    date = regex_date.fullmatch(date)
    if not date:
        print(f"Paramètre hour incorrect {date}")
        raise AttributeError
    return date


def date_to_int(date: str) -> int:
    """
        date: YYYY-MM-DD
    """
    return datetime.datetime(*map(int, date.split('-')))


def now():
    return datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
