from .. import f_entity


def test_dict():
    f = f_entity(id=1)
    assert f.__dict__ == {'id': 1, 'tags': {}, 'type': 'node', 'position': [0.0, 0.0]}
    f.doudou = 'test'
    f.owner = 'master'
    assert f.__dict__ == {'id': 1, 'tags': {}, 'doudou': 'test', 'type': 'node', 'position': [0.0, 0.0]}
