from . import Api_ext


class Osm(Api_ext):
    BASE_URL = 'http://overpass-api.de/api/interpreter'

    def call(self, query: str, city_name="Seyssinet-Pariset") -> dict:
        query = get_query(query, city_name=city_name, out_format="json", end="body")
        return super().call(data=query)


def get_query(query: str, city_name: str, out_format: str = "json", end: str = "body") -> bytes:
    ret = f'[out:"{out_format}"];\n'
    ret += f'area["name" = "{city_name}"]->.city;\n'
    ret += query
    ret += f'\nout {end};'
    return ret.encode('utf-8')
