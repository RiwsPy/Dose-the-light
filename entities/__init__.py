from typing import Any


class f_base(int):
    pass


class f_entity(f_base):
    def __new__(cls, **kwargs):
        return super().__new__(cls, kwargs['id'])

    def __init__(self, **kwargs) -> None:
        self.tags = {}
        self.owner = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, attr) -> Any:
        return self.tags.get(attr)

    @property
    def __dict__(self):
        cpy = super().__dict__.copy()
        try:
            del cpy['owner']
        except KeyError:
            pass
        return cpy
