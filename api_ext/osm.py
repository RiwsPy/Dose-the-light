from . import Api_ext


class Osm(Api_ext):
    BASE_URL = 'http://overpass-api.de/api/interpreter'

    def call(self, query: str, restr_area="Grenoble-Alpes Métropole", postal_code="38170") -> dict:
        query = get_query(query,
                          restr_area=restr_area,
                          postal_code=postal_code,
                          out_format="json",
                          end="body"
                          )
        return super().call(data=query)


def get_query(query: str,
              restr_area: str,
              postal_code: str,
              out_format: str = "json",
              end: str = "body") -> bytes:
    ret = f'[out:"{out_format}"];\n'
    ret += f'area["name" = "{restr_area}"]->.lim_area;\n'
    ret += f'area["name" = "{postal_code}"]->.city;\n'
    ret += query
    ret += f'\nout {end};'
    return ret.encode('utf-8')
