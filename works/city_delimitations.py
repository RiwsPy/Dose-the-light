from . import Works
from api_ext.osm import Osm


class City_delimitations(Works):
    db_filename = 'city_delimitations'
    call_method = Osm().call
    postal_code = "all"
    query = \
        """
        (
            relation(area.lim_area)[boundary=administrative][admin_level=8];
            node(r:"admin_centre");
        );
        """
