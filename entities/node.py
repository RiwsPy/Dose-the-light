from . import f_entity
from typing import Tuple
from .position import Position


class f_node(f_entity):
    def __init__(self, *args, **kwargs):
        self.lat = 0.0
        self.lon = 0.0
        super().__init__(*args, **kwargs)

    @property
    def position(self) -> Position:
        return Position((self.lat, self.lon))

    @position.setter
    def position(self, position: Tuple[float]) -> None:
        self.lat, self.lon = Position(position)
