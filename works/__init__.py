from formats.osm import f_osm
from formats.geojson import f_geojson
from api_ext.osm import call


class Works(f_osm):
    query = ""
    filename = "empty.json"
    call_method = call

    def update(self, filename=''):
        ret = self.call_method(self.query)
        if ret.get('features'):  # geojson
            f = f_geojson()
            f = f.load_and_create_osm(ret)
        elif ret.get('elements'):  # osm
            f = f_osm()
            f.loads(ret)
        else:
            raise TypeError
        f.dump(filename or self.filename)

    def load(self, filename=''):
        filename = filename or self.filename
        if type(filename) is str:
            super().load(filename)
        elif type(filename) is tuple:
            super().load(*filename)
