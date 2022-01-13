import requests
from . import BadStatusError


def call(self, query: str, city_name="Seyssinet-Pariset") -> dict:
    query = get_query(query, city_name=city_name, out_format="json", end="body")
    req = requests.request(method="GET",
                           url="http://overpass-api.de/api/interpreter",
                           data=query)
    if req.status_code != 200:
        print(f'ERROR status_code {req.status_code}')
        raise BadStatusError

    return req.json()


def get_query(query: str, city_name: str, out_format: str = "json", end: str = "body") -> str:
    ret = f'[out:"{out_format}"];\n'
    ret += f'area["name" = "{city_name}"]->.city;\n'
    ret += query
    ret += f'\nout {end};'
    return ret.encode('utf-8')
