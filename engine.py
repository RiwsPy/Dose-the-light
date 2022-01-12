#!/usr/bin/env python
from formats import osm

if __name__ == '__main__':
    f = osm.f_osm()
    f.load('base.json')
    f.dump('base2.json')
