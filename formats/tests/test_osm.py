from .. import osm
import pytest


@pytest.fixture
def setUp():
    yield osm.f_osm()


def test_create_base(setUp):
    assert setUp.osm3s['copyright'] == osm.COPYRIGHT


def test_append(setUp):
    setUp.append('1')
    assert setUp.elements == ['1']


def test_extend(setUp):
    setUp.extend(['1'])
    assert setUp.elements == ['1']


def test_load(setUp):
    setUp.load('base.json')
    node = setUp.elements[0]
    assert node.id == 136459
    way = setUp.elements[1]
    assert node in way.nodes
    relation = setUp.elements[2]
    assert node in relation.nodes
    assert way in relation.ways

    clone = setUp.__dict__.copy()
    setUp.load('base.json', 'empty.json')
    assert clone == setUp.__dict__
