from django.core.management.base import BaseCommand
from maps.models import Node, influencers_queryset, conflicts_queryset, City
import json
import os
from pathlib import Path
from collections import defaultdict
from entities.position import Position

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

db_files = {
    '38170_conflicts.json': {'is_conflict': True, 'is_influencer': False},
    '38170_opening_hours.json': {'is_conflict': False, 'is_influencer': True},
    '38170_public_building.json': {'is_conflict': False, 'is_influencer': True},
    '38170_residentials.json': {'is_conflict': False, 'is_influencer': True},

    '38170_worksites.json': {'is_conflict': True, 'is_influencer': False},
}


class Command(BaseCommand):
    help = 'Update database with json files in db/'

    def handle(self, *args, **kwargs) -> None:
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        reset()
        self.save_conflicts()
        self.save_cities()

    def save_conflicts(self):
        for filename in db_files:
            upload(filename)
        self.stdout.write(self.style.MIGRATE_HEADING('conflict in range en cours'))

        save_conflict_in_range()

        self.stdout.write(self.style.MIGRATE_HEADING(
            f'{Node.objects.all().count()} object(s) in db.'))
        self.stdout.write(self.style.MIGRATE_HEADING(
            f'{Node.objects.filter(is_influencer=True).count()} aimant(s) in db.'))
        self.stdout.write(self.style.MIGRATE_HEADING(
            f'{Node.objects.filter(is_conflict=True).count()} conflit(s) in db.'))

    def save_cities(self):
        with open(os.path.join(BASE_DIR, 'db/all_city_delimitations.json'), 'r') as file:
            data_objects = json.load(file)

        for data_city in data_objects['elements']:
            try:
                for postal_code in data_city['tags']['addr:postcode'].split(';'):
                    if postal_code:
                        new_city = City()
                        new_city.load(**data_city, postal_code=int(postal_code))
                        new_city.save()
            except KeyError:
                pass

        self.stdout.write(self.style.MIGRATE_HEADING(
            f'{City.objects.all().count()} cities in db.'))


def reset() -> None:
    Node.objects.all().delete()
    City.objects.all().delete()


def upload(filename: str) -> None:
    with open(os.path.join(BASE_DIR, 'db/' + filename), 'r') as file:
        data_objects = json.load(file)
    for obj in data_objects['elements']:
        obj['is_conflict'] = db_files[filename]['is_conflict']
        obj['is_influencer'] = db_files[filename]['is_influencer']
        node = Node()
        node.load(**obj)
        node.save()


def save_conflict_in_range() -> None:
    dict_save = defaultdict(list)
    influencers = influencers_queryset()
    for conflict in conflicts_queryset():
        pos_conflict = Position(list(conflict.position))
        for influencer in influencers:
            if pos_conflict.distance(list(influencer.position)) < 500:
                dict_save[influencer.id].append(conflict.id)

    with open(os.path.join(BASE_DIR, 'db/influ_conflicts.json'), 'w') as file:
        json.dump(dict_save, file)
