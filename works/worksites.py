from . import Works
from api_ext.grenoble_alpes_metropole import Gam
from entities.time import date_to_int, now


class Worksites(Works):
    db_filename = 'worksites'
    call_method = Gam().call
    url = 'opendata/Metro/ArretesEspacePublique/json/ARRETES_ESP_PUBLIQUE_VDG_EPSGE4326.json'

    def _can_be_output(self, obj) -> bool:
        begin_date = date_to_int(obj['tags']['Datedebtravaux'])
        end_date = date_to_int(obj['tags']['Datefintravaux'])
        return obj['tags']['ImpactCirculation'] and begin_date <= now() <= end_date
