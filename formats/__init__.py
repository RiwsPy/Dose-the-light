from typing import Any
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class base:
    data_attr = 'elements'
    ID = 1000000

    def __init__(self):
        setattr(self, self.data_attr, [])

    def __iter__(self):
        yield from getattr(self, self.data_attr)

    def __getitem__(self, value: int) -> Any:
        return getattr(self, self.data_attr)[getattr(self, self.data_attr).index(value)]

    def append(self, value: Any) -> None:
        getattr(self, self.data_attr).append(value)

    def extend(self, value: list) -> None:
        getattr(self, self.data_attr).extend(value)

    @classmethod
    def create_unique_id(cls) -> int:
        cls.ID += 1
        return cls.ID
