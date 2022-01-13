from typing import Tuple
from itertools import zip_longest
import math


class Position(Tuple[float]):
    default_pos = 0.0

    def __add__(self, other) -> 'Position':
        return self.__class__(
            pos1+pos2
            for pos1, pos2 in zip_longest(self, other, fillvalue=self.default_pos))

    def __truediv__(self, other) -> 'Position':
        return self.__class__(
            pos/other for pos in self
        )

    def distance(self, other) -> float:
        rm = 6371000  # Earth radius (meters)
        dlat_rad = math.radians(other[0]-self[0])
        dlon_rad = math.radians(other[1]-self[1])
        lat1_rad = math.radians(self[0])
        lat2_rad = math.radians(other[0])

        a = math.sin(dlat_rad/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon_rad/2)**2

        return rm * 2 * math.asin(a**0.5)
