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
        node.tags["conflicts"] = []
        conflict = node.tags.get('highway')
        if conflict:
            if conflict in self.highway_without_conflicts:
                return False
            if node.tags.get('public_transport') == 'platform':
                return False
            node.tags['conflicts'].append(conflict)
            return True

        type_conflict_intersection = []
        for way in node.ways:
            conflict_name = node.owner[way].tags.get('highway', '')
            type_conflict_intersection.append(conflict_name)
        if len(type_conflict_intersection) >= 3:
            txt = f'intersection: '
            for type_conflict in set(type_conflict_intersection):
                if type_conflict in ('motorway', 'trunk', 'primary', 'cycleway', 'steps',
                                     'secondary', 'tertiary', 'unclassified', 'residential'):
                    node.tags['conflicts'].append(txt + '-'.join(type_conflict_intersection))
                    return True
        return False

    def _can_be_output(self, obj) -> bool:
        return obj.type == 'node' and self.node_conflicts(obj)
