import requests
from . import BadStatusError


def call(self, url: str) -> dict:
    req = requests.request(method="GET",
                           url="http://entrepot.metropolegrenoble.fr/"+url)
    if req.status_code != 200:
        print('ERROR status_code', req.status_code)
        raise BadStatusError

    return req.json()
