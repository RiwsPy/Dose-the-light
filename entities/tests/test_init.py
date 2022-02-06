from .. import f_entity


def test_dict():
    f = f_entity(id=0)
    assert f.__dict__ == {'id': 0, 'tags': {}}
    f.doudou = 'test'
    f.owner = 'master'
    assert f.__dict__ == {'id': 0, 'tags': {}, 'doudou': 'test'}
