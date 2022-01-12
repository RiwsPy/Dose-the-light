from ..position import Position
import pytest


def test_position_create():
    pos = Position()
    assert pos == ()

    new_pos = (1.2982, 1.273)
    pos = Position(new_pos)
    assert pos == new_pos


def test_position_add():
    pos = Position((1, 2))
    adding_pos = (12.282, 2983)
    assert pos + adding_pos == (13.282, 2985)
