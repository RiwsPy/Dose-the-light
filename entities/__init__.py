from typing import Any


class f_base(int):
    pass


class f_entity(f_base):
    obj_type = 'node'
    obj_tags = 'tags'
    obj_default_tags = {'type': 'node', 'tags': {}}

    def __new__(cls, **kwargs):
        return super().__new__(cls, kwargs.get('id') or kwargs['properties']['pk'])

    def __init__(self, **kwargs) -> None:
        for k, v in self.obj_default_tags.copy().items():
            setattr(self, k, v)
        self.position = [0.0, 0.0]
        self.type = self.obj_type
        self.owner = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, attr) -> Any:
        return getattr(self, self.obj_tags, {}).get(attr)

    @property
    def __dict__(self):
        cpy = super().__dict__.copy()
        try:
            del cpy['owner']
        except KeyError:
            pass
        return cpy
