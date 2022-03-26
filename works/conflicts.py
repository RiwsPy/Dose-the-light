from . import Works
from api_ext.osm import Osm
from collections import defaultdict
from typing import DefaultDict


class Conflicts(Works):
    db_filename = 'conflicts'
    call_method = Osm().call
    skel_qt = True
    check_radius = 30  # in meters
    highway_without_conflicts = ('traffic_signals', 'give_way', )
    intersection_with_conflict = {'motorway', 'trunk', 'primary', 'cycleway', 'steps',
                                  'secondary', 'tertiary', 'unclassified', 'residential'}

    query = \
        f"""
        (
            (
                way(area.lim_area)(area.city)[highway][access!="private"][highway!=footway][highway!=service][highway!=platform][highway!=traffic_signals];
                way(area.lim_area)(area.city)[railway][railway!=abandoned][railway!=razed];
            )->.highway_items;
            node(around.highway_items:{check_radius})[highway][highway!="street_lamp"][highway!="traffic_signals"][highway!="give_way"][access!="private"];
        );
        """

    def output(self, filename: str = '', **kwargs) -> None:
        node_id_to_ways = defaultdict(list)
        for elt in self:
            if elt['type'] != 'way':
                continue

            for node in elt['nodes']:
                node_id_to_ways[node].append(elt)

        super().output(filename, node_id_to_ways=node_id_to_ways)

    def _can_be_output(self, node, node_id_to_ways) -> bool:
        if node['type'] != 'node':
            return False

        node['tags'] = node.get('tags', {})
        node['tags']["conflicts"] = node['tags'].get("conflicts", [])
        conflict_name = node['tags'].get('highway')

        if conflict_name:
            if conflict_name in self.highway_without_conflicts or\
                    node['tags'].get('public_transport') == 'platform':
                return False
        else:
            conflicts_type = [
                way['tags'].get('highway', '')
                for way in node_id_to_ways[node['id']]
            ]
            if not self.intersection_with_conflict.intersection(conflicts_type) or len(conflicts_type) < 3:
                return False
            conflict_name = '-'.join(
                                self.intersection_with_conflict.intersection(conflicts_type)
                                )
            conflict_name = 'intersection: ' + conflict_name

        node['tags']['conflicts'].append(conflict_name)
        return True
