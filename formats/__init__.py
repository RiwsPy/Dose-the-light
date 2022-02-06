from typing import Any
import json
from ..entities.node import f_node, f_node_geojson
from ..entities.way import f_way
from ..entities.relation import f_relation
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


class base:
    data_attr = 'elements'
    convert_type = {
        'node': f_node,
        'way': f_way,
        'relation': f_relation,
        'Point': f_node_geojson,
    }
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

    def dump(self,
             filename: str,
             ensure_ascii: bool = False,
             indent: int = 2) -> None:
        with open(os.path.join(BASE_DIR, 'db/' + filename + '.json'), 'w') as file:
            cpy = self.__dict__.copy()
            cpy[self.data_attr] = [
                obj.__dict__
                for obj in cpy[self.data_attr]]
            json.dump(cpy, file, ensure_ascii=ensure_ascii, indent=indent)

    def dumps(self) -> 'base':
        other = self.__class__()
        other.extend([
            obj.__dict__
            for obj in self])
        return other

    def load(self, *args: str) -> None:
        for index, filename in enumerate(args):
            with open(os.path.join(BASE_DIR, 'db/' + filename + '.json'), 'r') as file:
                if index:
                    self.extend(json.load(file)[self.data_attr])
                else:
                    for k, v in json.load(file).items():
                        setattr(self, k, v)
        self._rootinage()

    def loads(self, data: dict) -> None:
        for k, v in data.items():
            setattr(self, k, v)
        self._rootinage()

    @classmethod
    def create_unique_id(cls) -> int:
        cls.ID += 1
        return cls.ID

    def _rootinage(self) -> None:
        if self.data_attr == 'elements':
            setattr(self, self.data_attr, [
                self.convert_type.get(elt['type'], f_node)(**elt, owner=self)
                for index, elt in enumerate(self)
            ])
        elif self.data_attr == 'features':
            setattr(self, self.data_attr, [
                self.convert_type.get(elt['geometry']['type'], f_node_geojson)(**elt, owner=self)
                for index, elt in enumerate(self)
            ])

        elts = getattr(self, self.data_attr)
        for obj in self:
            if obj.type == 'way':
                obj.nodes = [
                    elts[elts.index(node)]
                    for node in obj.nodes]
                for node in obj.nodes:
                    node.ways.append(obj)

        for obj in self:
            if obj.type == 'relation':
                for member in obj.members:
                    member_id = elts[elts.index(member['ref'])]
                    if member['type'] == 'way':
                        obj.ways.append(member_id)
                        obj.nodes.extend(member_id.nodes)
                    elif member['type'] == 'node':
                        obj.nodes.append(member_id)
