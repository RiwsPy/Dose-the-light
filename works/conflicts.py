from . import Works
from api_ext.osm import call


class Conflicts(Works):
    filename = 'conflicts'
    call_method = call
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
    highway_without_conflicts = ('traffic_signals',)

    def node_conflicts(self, node) -> bool:
        conflict = node.tags.get('highway')
        return conflict and conflict not in self.highway_without_conflicts or len(set(node.ways)) >= 3

    def output(self):
        new_f = self.__class__()
        new_f.extend(
            [obj
             for obj in self
             if obj.type == 'node' and self.node_conflicts(obj)])
        new_f.dump(self.filename + '_output')
