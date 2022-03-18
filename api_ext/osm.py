from . import Api_ext


class Osm(Api_ext):
    BASE_URL = 'http://overpass-api.de/api/interpreter'

    def call(self,
             query: str,
             lim_area="Grenoble-Alpes Métropole",
             postal_code="38170",
             skel_qt=False) -> dict:
        query = get_query(query,
                          lim_area=lim_area,
                          postal_code=postal_code,
                          skel_qt=skel_qt,
                          out_format="json",
                          end="body"
                          )

        return super().call(data=query)


def get_query(query: str,
              lim_area: str,
              postal_code: str,
              skel_qt: bool,
              out_format: str,
              end: str) -> bytes:
    ret = f'[out:"{out_format}"];\n'
    ret += f'area["name" = "{lim_area}"]->.lim_area;\n'
    ret += f'area["postal_code" = "{postal_code}"]->.city;\n'
    ret += query
    ret += f'\nout {end};'
    if skel_qt:
        ret += '\n>;'
        ret += '\nout skel qt;'
    return ret.encode('utf-8')
