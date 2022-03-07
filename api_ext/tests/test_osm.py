from ..osm import Osm
import requests
from ...formats import osm
import pytest
from .. import BadStatusError


class Mock_request:
    def __init__(self, status_code: int):
        self.status_code = status_code

    @staticmethod
    def json():
        return osm.f_osm().__dict__


def test_call_ok(monkeypatch):
    def mock_get(*args, **kwargs):
        return Mock_request(200)

    monkeypatch.setattr(requests, "request", mock_get)
    req = Osm().call(query="")
    assert req['version'] == 0.6
    assert req['osm3s']['copyright'] == osm.COPYRIGHT
    assert req['elements'] == []


def test_call_fail(monkeypatch):
    def mock_get(*args, **kwargs):
        return Mock_request(404)

    monkeypatch.setattr(requests, "request", mock_get)
    with pytest.raises(BadStatusError):
        Osm().call(query="")
