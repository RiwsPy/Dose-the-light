from formats.osm import f_osm
from api_ext.osm import call


class Works(f_osm):
    query = ""
    filename = "empty.json"

    def update(self):
        ret = call(self.query)
        f = f_osm()
        f.loads(ret)
        f.dump(self.filename)
