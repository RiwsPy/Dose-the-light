from itertools import zip_longest
import math
from django.contrib.gis.geos import Point


class Position(Point):
    default_pos = 0.0

    def __iter__(self):
        yield from self.coords

    def __add__(self, other) -> 'Position':
        return self.__class__([
            pos1+pos2
            for pos1, pos2 in zip_longest(self, other, fillvalue=self.default_pos)])
    __iadd__ = __add__

    def __truediv__(self, other: float) -> 'Position':
        return self.__class__([
            pos/other for pos in self]
        )

    def __eq__(self, other) -> bool:
        return self.coords == getattr(other, 'coords', other)

    def distance(self, other) -> float:
        rm = 6371000  # Earth radius (meters)
        dlat_rad = math.radians(other[0]-self[0])
        dlon_rad = math.radians(other[1]-self[1])
        lat1_rad = math.radians(self[0])
        lat2_rad = math.radians(other[0])

        a = math.sin(dlat_rad/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon_rad/2)**2

        return rm * 2 * math.asin(a**0.5)
