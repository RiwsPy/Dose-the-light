from formats.osm import f_osm
from formats.geojson import f_geojson
from api_ext.osm import Osm
import json
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


class Works(dict):
    query = ""
    db_filename = "empty"
    file_ext = '.json'
    call_method = Osm().call
    data_attr = "elements"
    url = ""
    postal_code = "38170"
    skel_qt = False

    def __iter__(self):
        yield from self.features

    @property
    def iter_point(self):
        dict_id_node = {elt['id']: elt
                        for elt in self
                        }
        for elt in self:
            if elt['type'] == 'node':
                yield elt
            elif elt['type'] == 'way':
                cumul_lat, cumul_lon = 0, 0
                for search_node_id in elt['nodes']:
                    node = dict_id_node[search_node_id]
                    cumul_lat += node['lat']
                    cumul_lon += node['lon']
                center_lat = cumul_lat/len(elt['nodes'])
                center_lon = cumul_lon/len(elt['nodes'])
                elt['type'] = 'node'
                elt['lat'] = center_lat
                elt['lon'] = center_lon
                del elt['nodes']
                yield elt

    @property
    def features(self) -> list:
        return self[self.data_attr]

    def __len__(self) -> int:
        return len(self.features)

    @property
    def filename(self) -> str:
        return self.postal_code + '_' + self.db_filename

    def request(self, **kwargs) -> dict:
        kwargs = self._add_attr_in_kwargs('query', 'url', 'skel_qt', **kwargs)
        kwargs['postal_code'] = kwargs.get('postal_code', self.postal_code)

        return self.call_method(**kwargs)

    def _add_attr_in_kwargs(self, *args, **kwargs) -> dict:
        for attr in args:
            if attr not in kwargs and getattr(self, attr, False):
                kwargs[attr] = getattr(self, attr)
        return kwargs

    def update(self, **kwargs) -> None:
        super().update(convert_geojson_to_osm(kwargs))

    def load(self, filename='') -> None:
        with open(os.path.join(BASE_DIR, 'db/' + (filename or self.filename) + self.file_ext), 'r') as file:
            self.update(**json.load(file))

    def dump(self, filename='') -> None:
        with open(os.path.join(BASE_DIR, 'db/' + (filename or self.filename) + self.file_ext), 'w') as file:
            json.dump(self, file, ensure_ascii=False, indent=1)

    def output(self, filename='') -> None:
        new_f = self.__class__()
        new_f.update(**self)
        new_f[self.data_attr] = \
            [obj
             for obj in self.iter_point
             if self._can_be_output(obj)]
        new_f.dump(filename)

    def _can_be_output(self, obj) -> bool:
        return obj.get('tags', {}).get('name')


def convert_osm_to_geojson(data_dict: dict) -> dict:
    if 'features' in data_dict:
        return data_dict
    if 'elements' not in data_dict:
        raise KeyError

    ret = f_geojson()

    for elt in data_dict['elements']:
        if elt.get('_dont_copy'):
            continue

        elt_geojson = dict()
        elt_geojson['type'] = "Feature"
        elt_geojson['properties'] = elt.get('tags', {})
        if elt['type'] == 'node':
            elt_geojson['geometry'] = {'type': 'Point'}
            elt_geojson['geometry']['coordinates'] = [elt['lat'], elt['lon']]
        elif elt['type'] == 'way':
            elt_geojson['geometry'] = {}
            elt_geojson['geometry']['type'] = 'Polygon'
            elt_geojson['geometry']['coordinates'] = [[]]
            for search_node_id in elt['nodes']:
                for data_node in data_dict['elements']:
                    if data_node['id'] == search_node_id:
                        elt_geojson['geometry']['coordinates'][0].append([data_node['lon'], data_node['lat']])
                        data_node['_dont_copy'] = True
                        break

        ret.append(elt_geojson)
    return ret.__dict__


def convert_geojson_to_osm(data_dict: dict) -> dict:
    if 'elements' in data_dict:
        return data_dict
    if 'features' not in data_dict:
        raise KeyError

    f = f_osm()
    for elt in data_dict['features']:
        if elt['geometry']['type'] == 'Point':
            new_item = dict()
            new_item['type'] = 'node'
            new_item['lon'], new_item['lat'] = elt['geometry']['coordinates']
            new_item['id'] = f.create_unique_id()
            new_item['tags'] = elt['properties']
            f.append(new_item)
        else:
            print(elt['geometry']['type'], 'unknown')
    return f.__dict__
