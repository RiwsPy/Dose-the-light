from . import Works
from api_ext.osm import Osm


class Residentials(Works):
    db_filename = 'residentials'
    call_method = Osm().call
    # TODO: appliquer la contrainte [name] provoque une erreur 504
    query = \
        """
        (
            way(area.city)[landuse=residential];
        );
        (._;>;);
        """

    def _can_be_output(self, obj) -> bool:
        return obj.get('tags', {}).get('landuse') == 'residential'
