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
