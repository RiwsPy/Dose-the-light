from . import base


class f_osm(base):
    DB_ORIGIN = 'www.openstreetmap.org'
    DB_LICENSE = 'ODbL'
    data_attr = 'elements'

    def __init__(self):
        self.copyright = f'The data included in this document is from {self.DB_ORIGIN}.' +\
                         f' The data is made available under {self.DB_LICENSE}.'
        super().__init__()

    def mod_to_osm(self):
        return self

    @property
    def __dict__(self) -> dict:
        cpy = super().__dict__.copy()
        cpy[self.data_attr] = [
            obj
            for obj in cpy[self.data_attr]]
        return cpy
