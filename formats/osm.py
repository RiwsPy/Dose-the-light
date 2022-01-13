from datetime import datetime
import time
import json
from typing import Any
from entities.node import f_node
from entities.way import f_way
from entities.relation import f_relation

COPYRIGHT = 'The data included in this document is from www.openstreetmap.org.' +\
            ' The data is made available under ODbL.'


class f_osm:
    def __init__(self):
        self.version = 0.6
        self.generator = "Overpass API 0.7.57.1 74a55df1"
        self.osm3s = {
            "timestamp_osm_base": str(datetime.fromtimestamp(time.time())),
            "timestamp_areas_base": str(datetime.fromtimestamp(time.time())),
            'copyright': COPYRIGHT,
        }
        self.elements = []

    def append(self, value: Any) -> None:
        self.elements.append(value)

    def extend(self, value: list) -> None:
        self.elements.extend(value)

    def dump(self,
             filename: str,
             ensure_ascii: bool = False,
             indent: int = 2) -> None:
        with open('db/' + filename, 'w') as file:
            cpy = self.__dict__.copy()
            cpy['elements'] = [
                obj.__dict__
                for obj in cpy['elements']]
            json.dump(cpy, file, ensure_ascii=ensure_ascii, indent=indent)

    def load(self, *args: str) -> None:
        for index, filename in enumerate(args):
            with open('db/' + filename, 'r') as file:
                if index:
                    self.extend(json.load(file)['elements'])
                else:
                    for k, v in json.load(file).items():
                        setattr(self, k, v)
        self._rootinage()

    def loads(self, data: dict) -> None:
        for k, v in data.items():
            setattr(self, k, v)
        self._rootinage()

    def _rootinage(self) -> None:
        convert_type = {
            'node': f_node,
            'way': f_way,
            'relation': f_relation,
        }

        self.elements = [
            convert_type[elt['type']](**elt, owner=self)
            for index, elt in enumerate(self.elements)
        ]

        for obj in self.elements:
            if obj.type == 'way':
                obj.nodes = [
                    self.elements[self.elements.index(node)]
                    for node in obj.nodes]

        for obj in self.elements:
            if obj.type == 'relation':
                for member in obj.members:
                    member_id = self.elements[self.elements.index(member['ref'])]
                    if member['type'] == 'way':
                        obj.ways.append(member_id)
                        obj.nodes.extend(member_id.nodes)
                    elif member['type'] == 'node':
                        obj.nodes.append(member_id)
