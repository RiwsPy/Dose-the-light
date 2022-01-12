from typing import Tuple
from itertools import zip_longest


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
