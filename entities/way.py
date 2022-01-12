from . import f_entity
from .position import Position


class f_way(f_entity):
    @property
    def position(self) -> Position:
        # center position
        pos = Position()
        for node in self.nodes:
            pos += node.position
        return pos / len(self.nodes)

    @property
    def __dict__(self):
        cpy = super().__dict__.copy()
        try:
            del cpy['owner']
        except KeyError:
            pass
        return cpy
