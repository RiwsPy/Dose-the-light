#!/usr/bin/env python
from entities.position import Position
from works.conflicts import Conflicts
from works.worksites import Worksites
from works.opening_hours import Opening_hours
from works.public_buildings import Public_buildings
from works.residentials import Residentials

WORKS = (Conflicts, Worksites, Opening_hours, Public_buildings, Residentials)


def full_update():
    for work in WORKS:
        w = work()
        print(f'{w.db_filename} in progress')
        w.update(**w.request())
        w.dump()


def full_output():
    for work in WORKS:
        w = work()
        print(f'{w.db_filename} in progress')
        w.load()
        w.output()


if __name__ == '__main__':
    w = Conflicts()
    w.load()
    w.output()
    #show_conflicts('Tu 08:00')
    pass
