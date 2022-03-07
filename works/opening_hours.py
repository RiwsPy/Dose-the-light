from . import Works
from api_ext.osm import Osm


class Opening_hours(Works):
    db_filename = 'opening_hours'
    call_method = Osm().call
    query = \
        """
        (
            node(area.lim_area)(area.city)[opening_hours][opening_hours!='24/7'][access!="private"];
            way(area.lim_area)(area.city)[opening_hours][opening_hours!='24/7'][access!="private"];
        );
        (._;>;);
        """
