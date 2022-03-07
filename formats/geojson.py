from . import base


class f_geojson(base):
    data_attr = 'features'

    def __init__(self):
        self.COPYRIGHT = ""
        self.type = "FeatureCollection"
        super().__init__()
