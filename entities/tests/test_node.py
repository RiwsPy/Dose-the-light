from ..node import f_node


def test_create():
    node = f_node(id=0)
    assert node.lat == 0.0
    assert node.lon == 0.0


def test_node_position():
    node = f_node(id=0)
    assert node.position == (0.0, 0.0)
    new_pos = (12.21, 873.223)
    node.position = new_pos
    assert node.position == new_pos
    assert node.lat == new_pos[0]
    assert node.lon == new_pos[1]


def test_opening_hours():
    node = f_node(id=0)
    assert not node.opening_hours
    node.tags['opening_hours'] = 'Mo 09:00-14:00'
    assert node.opening_hours == {
        'Mo': ['09:00-14:00'],
        'Tu': [],
        'We': [],
        'Th': [],
        'Fr': [],
        'Sa': [],
        'Su': [],
    }


def test_is_open():
    node = f_node(id=0)
    assert not node.opening_hours
    node.tags['opening_hours'] = 'Mo 09:00-14:00'
    assert node.is_open('Mo 10:00')
    assert not node.is_open('Tu 10:00')
    assert not node.is_open('Mo 15:00')


def test_in_rush_hour():
    node = f_node(id=0)
    node.tags['opening_hours'] = 'Mo 09:00-14:00'
    assert node.in_rush_hour('Mo 09:00')
    assert node.in_rush_hour('Mo 08:00')
    assert node.in_rush_hour('Mo 14:59')
    assert not node.in_rush_hour('Mo 12:00')
    assert not node.in_rush_hour('Mo 15:00')
    assert not node.in_rush_hour('Mo 07:00')
    assert not node.in_rush_hour('Tu 08:00')


def test_coef_rush():
    node = f_node(id=0)
    node.tags['opening_hours'] = 'Mo 09:00-14:00'
    assert node.coef_rush('Mo 09:00') == 3
    assert node.coef_rush('Mo 07:00') == 0
    assert node.coef_rush('Mo 12:00') == 1
    node.tags['shop'] = 'supermarket'
    assert node.coef_rush('Mo 12:00') == 2

