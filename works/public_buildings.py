from . import Works
from api_ext.osm import call
from typing import Tuple, Any
from entities.node import f_node


class Public_buildings(Works):
    filename = 'public_building'
    call_method = call
    query = \
        f"""
        (
            nwr(area.city)[amenity=kindergarten];
            nwr(area.city)[amenity=childcare];
            nwr(area.city)[amenity=school];
            nwr(area.city)[amenity=college];
            nwr(area.city)[amenity=fire_station];
            nwr(area.city)[amenity=police];
            nwr(area.city)[amenity=hospital];
        );
        (._;>;);
        """

    def output(self, filename=''):
        new_f = self.__class__()
        elements = []
        for obj in self:
            can_be_added, new_obj = self._can_be_output(obj)
            if can_be_added:
                elements.append(new_obj)
        new_f.extend(elements)
        new_f.dump(filename or self.filename + '_output')

    def _can_be_output(self, obj) -> Tuple[bool, Any]:
        if obj.type == 'node':
            return not obj.ways, obj
        elif obj.type == 'way':
            new_node = f_node(id=obj.id)
            new_node.position = obj.position
            new_node.tags = obj.tags
            return True, new_node
        return False, obj
