import pytest
from ..node import date_check, time_slot_int, hour_int


def test_date_check():
    date = date_check('Mo 15:32')
    assert date.group('day') == 'Mo'
    assert date.group('hour') == '15:32'

    with pytest.raises(AttributeError):
        date_check('PP 09:00')
        date_check('Mo 09:0')
        date_check('Mo 9:00')
        date_check('Mo 09h00')


def test_time_slot_int():
    assert time_slot_int('09:00-10:00') == (9.0, 10.0)
    assert time_slot_int('09:30-10:00') == (9.5, 10.0)
    assert time_slot_int('18:15-19:45') == (18.25, 19.75)

    with pytest.raises(AttributeError):
        time_slot_int('09:00')
        time_slot_int('09:00-10')


def test_hour_int():
    assert hour_int('09:00') == 9.0
    assert hour_int('10:30') == 10.5
    assert hour_int('20:12') == 20.2
    assert hour_int('9:00') == 9.0

    with pytest.raises(AttributeError):
        hour_int('09h00')
