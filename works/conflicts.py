from . import Works


class Conflicts(Works):
    filename = 'conflicts.json'
    check_radius = 30  # in meters
    query = \
        f"""
        (
            (
                way(area.city)[highway][access!="private"][highway!=footway][highway!=service][highway!=platform][highway!=traffic_signals];
                way(area.city)[railway][railway!=abandoned][railway!=razed];
            )->.highway_items;
            node(around.highway_items:{check_radius})[highway][highway!="street_lamp"][access!="private"];
        );
        (._;>;);
        """

    def find(self, date: str):
        pass
