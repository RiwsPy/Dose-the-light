from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core import serializers
from entities.time import time_slot_int, hour_int, Opening_hours, building_opening_hours
from typing import Dict
import json
from django.db.models import QuerySet
import re


class Node(models.Model):
    """
        An impacting node
    """
    id = models.IntegerField(primary_key=True)
    position = models.PointField(default=Point(0, 0))
    is_conflict = models.BooleanField(default=True)
    is_influencer = models.BooleanField(default=False)
    conflicts_value = models.IntegerField(default=0)
    conflicts_details = models.TextField(default="")

    opening_hours = models.CharField(max_length=255, default="")
    name = models.CharField(max_length=255, default="")
    amenity = models.CharField(max_length=255, default="")
    highway = models.CharField(max_length=255, default="")
    shop = models.CharField(max_length=255, default="")
    landuse = models.CharField(max_length=255, default="")
    public_transport = models.CharField(max_length=255, default="")
    bus = models.CharField(max_length=255, default="")
    railway = models.CharField(max_length=255, default="")

    # description ?
    details = models.CharField(max_length=255, default="")

    @property
    def pr_dict(self) -> dict:
        clone_dict = self.__dict__.copy()
        del clone_dict['_state']
        position = clone_dict['position']
        del clone_dict['position']
        new_dict = dict()
        new_dict['properties'] = clone_dict
        new_dict['geometry'] = {'coordinates': list(position)}
        return new_dict

    def load(self, **kwargs):
        new_attrs = dict(**kwargs.get('tags', {}), **kwargs)
        new_attrs['position'] = Point(kwargs['lat'], kwargs['lng'])
        new_attrs['conflicts_details'] = new_attrs.get('conflicts_details', '') +\
            '\n'.join(new_attrs.get('conflicts', []))

        for k, v in new_attrs.items():
            setattr(self, k, v)

    @staticmethod
    def serialize(queryset, file_format: str = "geojson") -> dict:
        return json.loads(serializers.serialize(file_format, queryset))

    @property
    def _opening_hours(self) -> Dict[str, list]:
        if type(self.opening_hours) is str:
            if not self.opening_hours:
                self.opening_hours = self.special_opening_hours()
            else:
                self.opening_hours = Opening_hours(self.opening_hours).__dict__

        return self.opening_hours

    def special_opening_hours(self) -> dict:
        if self.amenity == 'school':
            return building_opening_hours.school
        elif self.amenity == 'college':
            return building_opening_hours.college
        elif self.landuse == 'residential':
            return building_opening_hours.residential
        elif self.public_transport == 'stop_position' and self.bus == "yes":
            return building_opening_hours.bus_station
        elif self.railway == "yes":
            return building_opening_hours.tram_station
        elif self.amenity in ('childcare', 'kindergarten'):
            return building_opening_hours.childcare
        return {}

    def is_open(self, date: str) -> bool:
        if self.amenity in ('police', 'fire_station', 'hospital'):
            return True

        opening_hours = self._opening_hours
        int_hour = hour_int(date.group('hour'))
        for opening_hour in opening_hours.get(date.group('day'), []):
            time_min, time_max = time_slot_int(opening_hour)
            if time_min <= int_hour <= time_max:
                return True

        return not opening_hours

    def in_rush_hour(self, date: re.Match) -> bool:
        # TODO: gestion des heures +1/-1 incorrectes sur des horaires proches de minuit
        opening_hours = self._opening_hours

        if not opening_hours or date.group('day') not in opening_hours or not opening_hours[date.group('day')]:
            return False
        int_hour = hour_int(date.group('hour'))
        time_min = time_slot_int(opening_hours[date.group('day')][0])[0]
        time_max = time_slot_int(opening_hours[date.group('day')][-1])[-1]

        if time_min == 0 and time_max == 24:  # 24/7
            return False
        elif self.landuse == 'residential' and\
                (time_min - 1 <= int_hour < time_min + 2 or
                 time_max - 2 <= int_hour < time_max + 1):
            return True
        elif time_min - 1 <= int_hour < time_min + 1 or \
                time_max - 1 <= int_hour < time_max + 1:
            return True

        return False

    def coef_rush(self, date: re.Match) -> int:
        # TODO: 1 même entre midi et 14h en cas de fermeture

        if self.in_rush_hour(date):
            if self.landuse == "residential":
                return 5
            return 3
        if self.is_open(date):
            if self.shop == 'supermarket':
                return 2
            return 1
        return 0


def influencers_queryset() -> QuerySet:
    return Node.objects.filter(is_influencer=True)


def conflicts_queryset() -> QuerySet:
    return Node.objects.filter(is_conflict=True)
