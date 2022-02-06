#!/usr/bin/env python
from formats import f_osm
from entities import f_node
from works import Conflicts
from works import Worksites
from works.opening_hours import Opening_hours
from works.public_buildings import Public_buildings
from works.residentials import Residentials
import math

WORKS = (Conflicts, Worksites, Opening_hours, Public_buildings, Residentials)


def show_conflicts(date: str):
    # fond : 2200 conflits, 950 dû à l'heure
    cf = Conflicts()
    cf.load(filename=cf.filename+'_output')
    wk = Worksites()
    wk.load(filename=wk.filename+'_output')
    oh = Opening_hours()
    oh.load(filename=oh.filename+'_output')
    pb = Public_buildings()
    pb.load(filename=pb.filename+'_output')
    rd = Residentials()
    rd.load(filename=rd.filename+'_output')

    cf.extend(wk.elements)
    oh.extend(rd.elements)
    oh.extend(pb.elements)
    print(len(cf.elements), 'zones de conflits potentielles')
    print(len(oh.elements), 'aimants relevés')

    f = f_osm()
    nb = 0
    for conflict in cf:
        if conflict._opening_hours and not conflict.is_open(date):
            continue
        f.append(conflict)
        nb_activation = 0
        for shop in oh:
            if nb_activation > 2:
                break
            coef = shop.coef_rush(date)
            if coef and conflict.position.distance(shop.position) < 200:
                coef /= 10
                conflict.tags['conflicts'].append(shop.tags.get('name', str(shop.id)) + f'({coef})')
                nb_activation += coef
        for _ in range(math.ceil(nb_activation)):
            nb += 1
            new_node = f_node(id=f.create_unique_id())
            new_node.position = conflict.position + (0.00001, 0.00001)
            new_node.tags = conflict.tags
            f.append(new_node)
    print(nb, 'influence de heure')
    print(len(f.elements), 'conflits relevés')
    f.dump('conflicts_with_timing_output')


def full_update():
    for work in WORKS:
        print(f'{work} in progress')
        work().update()


def full_output():
    for work in WORKS:
        print(f'{work} in progress')
        w = work()
        w.load()
        w.output()


if __name__ == '__main__':
    #w = Public_buildings()
    #w.load()
    #w.output()
    show_conflicts('Tu 08:00')
    pass
