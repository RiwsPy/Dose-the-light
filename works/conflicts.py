from . import Works
from api_ext.osm import Osm
from collections import defaultdict


class Conflicts(Works):
    db_filename = 'conflicts'
    call_method = Osm().call
    check_radius = 30  # in meters
    highway_without_conflicts = ('traffic_signals', 'give_way', )
    query = \
        f"""
        (
            (
                way(area.lim_area)(area.city)[highway][access!="private"][highway!=footway][highway!=service][highway!=platform][highway!=traffic_signals];
                way(area.lim_area)(area.city)[railway][railway!=abandoned][railway!=razed];
            )->.highway_items;
            node(around.highway_items:{check_radius})[highway][highway!="street_lamp"][access!="private"];
        );
        (._;>;);
        """

    def output(self, filename='') -> None:
        dict_id_to_way = {}
        dict_node_ways = defaultdict(list)
        for elt in self:
            if elt['type'] == 'way':
                dict_id_to_way[elt['id']] = elt
                for node in elt['nodes']:
                    dict_node_ways[node].append(elt['id'])

        new_f = self.__class__()
        new_f.update(**self)
        new_f[self.data_attr] = \
            [obj
             for obj in self
             if self.node_conflicts(obj, dict_node_ways, dict_id_to_way)]
        new_f.dump(filename)

    def node_conflicts(self, node, dict_node_ways, dict_id_to_way) -> bool:
        if node['type'] != 'node':
            return False

        node['tags'] = node.get('tags', {})
        node['tags']["conflicts"] = node['tags'].get("conflicts", [])
        conflict = node['tags'].get('highway')
        if conflict:
            if conflict in self.highway_without_conflicts:
                return False
            if node['tags'].get('public_transport') == 'platform':
                return False
            node['tags']['conflicts'].append(conflict)
            return True

        type_conflict_intersection = []
        for way in dict_node_ways[node['id']]:
            conflict_name = dict_id_to_way[way]['tags'].get('highway', '')
            type_conflict_intersection.append(conflict_name)
        if len(type_conflict_intersection) >= 3:
            txt = f'intersection: '
            for type_conflict in set(type_conflict_intersection):
                if type_conflict in ('motorway', 'trunk', 'primary', 'cycleway', 'steps',
                                     'secondary', 'tertiary', 'unclassified', 'residential'):
                    node['tags']['conflicts'].append(txt + '-'.join(type_conflict_intersection))
                    return True
        return False

