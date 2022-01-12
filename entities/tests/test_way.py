from ..way import f_way
from ..node import f_node


def test_create():
    way = f_way(id=0, nodes=[])
    assert not way.position

    new_node = f_node(id=1)
    pos = (2, 3)
    new_node.position = pos
    way.nodes.append(new_node)
    assert way.position == pos

    new_node = f_node(id=2)
    pos = (4, 5)
    new_node.position = pos
    way.nodes.append(new_node)
    assert way.position == (3, 4)
