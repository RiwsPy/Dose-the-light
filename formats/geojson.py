from . import base
from .osm import f_osm
from entities.node import f_node


class f_geojson(base):
    data_attr = 'features'

    def __init__(self):
        self.name = ""
        self.type = ""
        super().__init__()

    def load_and_create_osm(self, data) -> f_osm:
        for k, v in data.items():
            setattr(self, k, v)

        f = f_osm()
        for elt in self:
            if elt['geometry']['type'] == 'Point':
                new_item = f_node(id=f.create_unique_id())
                new_item.tags = elt['properties']
                new_item.type = 'node'
                new_item.tags.update(elt['properties'])
                new_item.lat = elt['geometry']['coordinates'][1]
                new_item.lon = elt['geometry']['coordinates'][0]
                f.append(new_item)
            else:
                print(elt['geometry']['type'], 'unknown')

        return f
