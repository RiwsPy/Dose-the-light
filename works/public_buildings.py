from . import Works
from api_ext.osm import Osm


class Public_buildings(Works):
    db_filename = 'public_building'
    call_method = Osm().call
    query = \
        """
        (
            nwr(area.lim_area)(area.city)[amenity=kindergarten];
            nwr(area.lim_area)(area.city)[amenity=childcare];
            nwr(area.lim_area)(area.city)[amenity=school];
            nwr(area.lim_area)(area.city)[amenity=college];
            nwr(area.lim_area)(area.city)[amenity=fire_station];
            nwr(area.lim_area)(area.city)[amenity=police];
            nwr(area.lim_area)(area.city)[amenity=hospital];
            nwr(area.lim_area)(area.city)[amenity=place_of_worship];
        );
        (._;>;);
        """
