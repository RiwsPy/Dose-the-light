from typing import Any
import random
import json
from entities.node import f_node
from entities.way import f_way
from entities.relation import f_relation
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


class base:
    data_attr = 'elements'

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

    def create_unique_id(self) -> int:
        nb = 1000000
        while nb in self:
            nb = random.randint(1000001, 10000000)
        return nb

    def _rootinage(self) -> None:
        convert_type = {
            'node': f_node,
            'way': f_way,
            'relation': f_relation,
        }
        setattr(self, self.data_attr, [
            convert_type[elt['type']](**elt, owner=self)
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
