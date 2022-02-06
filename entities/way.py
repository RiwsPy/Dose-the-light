from . import f_entity
from .position import Position


class f_way(f_entity):
    def __init__(self, *args, **kwargs):
        self.type = 'way'
        super().__init__(*args, **kwargs)

    @property
    def position(self) -> Position:
        # center position
        pos = Position()
        for node in self.nodes:
            pos += node.position
        return pos / len(self.nodes)

    @position.setter
    def position(self, value) -> None:
        pass
