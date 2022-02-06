from . import Works
from api_ext.osm import call
from entities.node import f_node


class Opening_hours(Works):
    filename = 'opening_hours'
    call_method = call
    query = \
        """
        (
            node(area.city)[opening_hours][opening_hours!='24/7'][access!="private"];
            way(area.city)[opening_hours][opening_hours!='24/7'][access!="private"];
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

    def _can_be_output(self, obj) -> tuple:
        if obj.type == 'node':
            return not obj.ways, obj
        elif obj.type == 'way':
            new_node = f_node(id=obj.id)
            new_node.position = obj.position
            new_node.tags = obj.tags
            return True, new_node
        return False, obj

