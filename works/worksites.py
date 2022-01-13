from . import Works
from api_ext.grenoble_alpes_metropole import call
from entities.time import date_to_int, now


class Worksites(Works):
    filename = 'worksites'
    call_method = call
    query = 'opendata/Metro/ArretesEspacePublique/json/ARRETES_ESP_PUBLIQUE_VDG_EPSGE4326.json'

    @staticmethod
    def node_is_open_and_trouble(node) -> bool:
        begin_date = date_to_int(node.tags['Datedebtravaux'])
        end_date = date_to_int(node.tags['Datefintravaux'])
        return node.tags['ImpactCirculation'] and begin_date <= now() <= end_date

    def _can_be_output(self, obj) -> bool:
        return obj.type == 'node' and self.node_is_open_and_trouble(obj)
