from . import Works
from api_ext.grenoble_alpes_metropole import call
from entities.time import date_to_int, now


class Worksites(Works):
    filename = 'worksites'
    call_method = call
    query = 'opendata/Metro/ArretesEspacePublique/json/ARRETES_ESP_PUBLIQUE_VDG_EPSGE4326.json'

    def output(self):
        new_f = self.__class__()
        new_f.call_method = 'elements'
        new_f.extend(
            [obj
             for obj in self
             if obj.type == 'node' and self.node_is_open_and_trouble(obj)])
        new_f.dump(self.filename + '_output')

    @staticmethod
    def node_is_open_and_trouble(node) -> bool:
        begin_date = date_to_int(node.tags['Datedebtravaux'])
        end_date = date_to_int(node.tags['Datefintravaux'])
        return node.tags['ImpactCirculation'] and begin_date <= now() <= end_date
