from . import f_entity
from .position import Position
from typing import Any


class f_node(f_entity):
    obj_type = 'node'
    obj_tags = 'tags'
    obj_default_tags = {'type': 'node', 'tags': {}}

    def __init__(self, **kwargs):
        self.ways = []
        super().__init__(**kwargs)

    def __getattr__(self, attr) -> Any:
        return self.tags.get(attr)

    @property
    def position(self) -> Position:
        return Position((self.lat, self.lon))

    @position.setter
    def position(self, position: Position) -> None:
        self.lat, self.lon = position


class f_node_geojson(f_node):
    obj_type = 'Feature'
    obj_default_tags = {'properties': {}, 'geometry': {'type': 'Point'}}

    def __getattr__(self, attr) -> Any:
        return self.properties.get(attr)

    @property
    def position(self) -> Position:
        return Position(self.geometry['coordinates'])

    @position.setter
    def position(self, position: Position) -> None:
        self.geometry['coordinates'] = position
