from . import Works
from api_ext.osm import call
from entities.time import regex_days, regex_hours


class Opening_hours(Works):
    filename = 'opening_hours'
    call_method = call
    query = \
        """
        (
            node(area.city)[opening_hours][opening_hours!='24/7'][access!="private"];
        );
        """

    def _can_be_output(self, obj) -> bool:
        return True
