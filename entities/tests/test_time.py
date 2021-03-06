import pytest
from ..time import date_check, time_slot_int, hour_int, date_percent_in_week


def test_date_check():
    date = date_check('Mo 15:32')
    assert date.group('day') == 'Mo'
    assert date.group('hour') == '15:32'

    with pytest.raises(AttributeError):
        date_check('PP 09:00')
    with pytest.raises(AttributeError):
        date_check('Mo 09:0')
    with pytest.raises(AttributeError):
        date_check('Mo 9:00')
    with pytest.raises(AttributeError):
        date_check('Mo 09h00')


def test_time_slot_int():
    assert time_slot_int('09:00-10:00') == (9.0, 10.0)
    assert time_slot_int('09:30-10:00') == (9.5, 10.0)
    assert time_slot_int('18:15-19:45') == (18.25, 19.75)

    with pytest.raises(AttributeError):
        time_slot_int('09:00')
    with pytest.raises(AttributeError):
        time_slot_int('09:00-10')


def test_hour_int():
    assert hour_int('09:00') == 9.0
    assert hour_int('10:30') == 10.5
    assert hour_int('20:12') == 20.2
    assert hour_int('9:00') == 9.0

    with pytest.raises(AttributeError):
        hour_int('09h00')


def test_date_percent_in_week():
    assert date_percent_in_week('Mo 00:00') == 0.0
    assert date_percent_in_week('Mo 08:00') == 4.761904761904762
    assert date_percent_in_week('Su 24:00') == 100.0
