from . import f_entity
from .position import Position
from typing import Dict, Any
from .time import date_check, time_slot_int, hour_int, Opening_hours
from .time import building_opening_hours


class f_node(f_entity):
    def __init__(self, **kwargs):
        self.lat = 0.0
        self.lon = 0.0
        self.type = 'node'
        self.ways = []
        super().__init__(**kwargs)

    @property
    def position(self) -> Position:
        return Position((self.lat, self.lon))

    @position.setter
    def position(self, position: Position) -> None:
        self.lat, self.lon = position

    @property
    def _opening_hours(self) -> Dict[str, list]:
        if not self.opening_hours:
            return self.special_opening_hours()

        return Opening_hours(self.opening_hours).__dict__

    def special_opening_hours(self) -> dict:
        if self.amenity == 'school':
            return building_opening_hours.school
        elif self.amenity == 'college':
            return building_opening_hours.college
        elif self.landuse == 'residential':
            return building_opening_hours.residential
        elif self.public_transport == 'stop_position' and self.bus == "yes":
            return building_opening_hours.bus_station
        elif self.railway == "yes":
            return building_opening_hours.tram_station
        elif self.amenity in ('childcare', 'kindergarten'):
            return building_opening_hours.childcare
        return {}

    def is_open(self, date: str) -> bool:
        if self.amenity in ('police', 'fire_station', 'hospital'):
            return True
        date = date_check(date)
        opening_hours = self._opening_hours
        int_hour = hour_int(date.group('hour'))
        for opening_hour in opening_hours.get(date.group('day'), []):
            time_min, time_max = time_slot_int(opening_hour)
            if time_min <= int_hour <= time_max:
                return True

        return not opening_hours

    def in_rush_hour(self, date: str) -> bool:
        # TODO: gestion des heures +1/-1 incorrectes sur des horaires proches de minuit
        date = date_check(date)
        opening_hours = self._opening_hours
        if not opening_hours or date.group('day') not in opening_hours or not opening_hours[date.group('day')]:
            return False
        int_hour = hour_int(date.group('hour'))
        time_min = time_slot_int(opening_hours[date.group('day')][0])[0]
        time_max = time_slot_int(opening_hours[date.group('day')][-1])[-1]

        if time_min == 0 and time_max == 24:  # 24/7
            return False
        elif self.landuse == 'residential' and\
                (time_min - 1 <= int_hour < time_min + 2 or
                 time_max - 2 <= int_hour < time_max + 1):
            return True
        elif time_min - 1 <= int_hour < time_min + 1 or \
                time_max - 1 <= int_hour < time_max + 1:
            return True

        return False

    def coef_rush(self, date: str) -> int:
        # TODO: 1 même entre midi et 14h en cas de fermeture
        date_check(date)
        if self.in_rush_hour(date):
            if self.landuse == "residential":
                return 5
            return 3
        if self.is_open(date):
            if self.shop == 'supermarket':
                return 2
            return 1
        return 0
