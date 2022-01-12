import requests
from . import BadStatusError


def call(query: str) -> dict:
    query = '[out:"json"];' + query
    query = query.encode('utf-8')
    req = requests.request(method="GET",
                           url="http://overpass-api.de/api/interpreter",
                           data=query)
    if req.status_code != 200:
        print('ERROR status_code', req.status_code)
        raise BadStatusError

    return req.json()


