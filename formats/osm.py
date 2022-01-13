from datetime import datetime
import time
import json
from entities.node import f_node
from entities.way import f_way
from entities.relation import f_relation
from . import base

COPYRIGHT = 'The data included in this document is from www.openstreetmap.org.' +\
            ' The data is made available under ODbL.'


class f_osm(base):
    data_attr = 'elements'

    def __init__(self):
        self.version = 0.6
        self.generator = "Overpass API 0.7.57.1 74a55df1"
        self.osm3s = {
            "timestamp_osm_base": str(datetime.fromtimestamp(time.time())),
            "timestamp_areas_base": str(datetime.fromtimestamp(time.time())),
            'copyright': COPYRIGHT,
        }
        super().__init__()

    def mod_to_osm(self):
        return self
