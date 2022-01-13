from . import f_entity
from typing import Tuple
from .position import Position
import re
from typing import Dict
from .time import date_check, time_slot_int, hour_int

days = ('Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su')
regex_data_day = re.compile(r'; *')
regex_days = re.compile(r'(Mo|Tu|We|Th|Fr|Sa|Su)(-|, )?(Mo|Tu|We|Th|Fr|Sa|Su)?')
regex_hours = re.compile(r'\d\d:\d\d-\d\d:\d\d')
regex_time_slot = re.compile(r'(?P<h1>\d\d):(?P<m1>\d\d)-(?P<h2>\d\d):(?P<m2>\d\d)')


class f_node(f_entity):
    def __init__(self, *args, **kwargs):
        self.lat = 0.0
        self.lon = 0.0
        self.ways = []
        super().__init__(*args, **kwargs)

    @property
    def position(self) -> Position:
        return Position((self.lat, self.lon))

    @position.setter
    def position(self, position: Tuple[float]) -> None:
        self.lat, self.lon = Position(position)

    @property
    def opening_hours(self) -> Dict[str, list]:
        opening_hours = self.tags.get('opening_hours')
        if not opening_hours:
            return {}

        ret = default_opening_hours()
        for opening_days in re.split(regex_data_day, opening_hours):
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

    def is_open(self, date: str) -> bool:
        date = date_check(date)
        opening_hours = self.opening_hours
        int_hour = hour_int(date.group('hour'))
        for opening_hour in opening_hours.get(date.group('day'), []):
            time_min, time_max = time_slot_int(opening_hour)
            if time_min <= int_hour <= time_max:
                return True

        return not opening_hours

    def in_rush_hour(self, date: str) -> bool:
        # TODO: gestion des heures +1/-1 incorrectes sur des horaires proches de minuit
        date = date_check(date)
        opening_hours = self.opening_hours
        if not opening_hours or date.group('day') not in opening_hours:
            return False
        date_hour = hour_int(date.group('hour'))
        for opening_hour in opening_hours[date.group('day')]:
            h_min, h_max = time_slot_int(opening_hour)
            if h_min - 1 <= date_hour < h_min + 1 or\
                    h_max - 1 <= date_hour < h_max + 1:
                return True

        return False

    def coef_rush(self, date: str) -> int:
        date_check(date)
        if self.in_rush_hour(date):
            return 3
        if self.is_open(date):
            if self.tags.get('shop') == 'supermarket':
                return 2
            return 1
        return 0


def default_opening_hours(string: str = '') -> dict:
    if string == '':
        return {
            day: []
            for day in days}

    return {
        day: [string]
        for day in days}
