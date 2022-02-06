from . import Works
from api_ext.osm import call
from typing import Any, Tuple
from entities.node import f_node


class Residentials(Works):
    filename = 'residentials'
    call_method = call
    # TODO: appliquer la contrainte [name] provoque une erreur 504
    query = \
        """
        (
            way(area.city)[landuse=residential];
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
        if obj.type == 'way' and obj.tags.get('name'):
            new_node = f_node(id=obj.id)
            new_node.position = obj.position
            new_node.tags = obj.tags
            return True, new_node
        return False, obj
