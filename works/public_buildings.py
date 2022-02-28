from . import Works
from api_ext.osm import Osm


class Public_buildings(Works):
    db_filename = 'public_building'
    call_method = Osm().call
    query = \
        """
        (
            nwr(area.city)[amenity=kindergarten];
            nwr(area.city)[amenity=childcare];
            nwr(area.city)[amenity=school];
            nwr(area.city)[amenity=college];
            nwr(area.city)[amenity=fire_station];
            nwr(area.city)[amenity=police];
            nwr(area.city)[amenity=hospital];
            nwr(area.city)[amenity=place_of_worship];
        );
        (._;>;);
        """
