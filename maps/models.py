from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core import serializers
from entities.time import time_slot_int, hour_int, Opening_hours, building_opening_hours
from typing import Dict
import json
from django.db.models import QuerySet
import re
import os
from dosethelight.settings import BASE_DIR


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

    opening_hours = models.CharField(max_length=255, default="")  # 'Mo 08:00-20:00'
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
        new_dict = dict()
        new_dict['type'] = "Feature"
        new_dict['geometry'] = {'coordinates': list(clone_dict['position'])[::-1], 'type': 'Point'}

        del clone_dict['_state']
        del clone_dict['position']
        new_dict['properties'] = clone_dict
        return new_dict

    def load(self, **kwargs):
        new_attrs = dict(**kwargs.get('tags', {}), **kwargs)
        new_attrs['position'] = Point(kwargs['lat'], kwargs['lon'])
        new_attrs['conflicts_details'] = new_attrs.get('conflicts_details', '') +\
            '\n'.join(new_attrs.get('conflicts', []))

        for k, v in new_attrs.items():
            setattr(self, k, v)

    @staticmethod
    def serialize(queryset, file_format: str = "geojson") -> dict:
        ret = json.loads(serializers.serialize(file_format, queryset))
        del ret['crs']
        return ret

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

    def is_open(self, date: re.Match) -> bool:
        if self.is_always_open:
            return True

        opening_hours = self._opening_hours
        int_hour = hour_int(date.group('hour'))
        for opening_hour in opening_hours.get(date.group('day'), []):
            time_min, time_max = time_slot_int(opening_hour)
            if time_min <= int_hour <= time_max:
                return True

        return not opening_hours

    def is_open_or_on_break(self, date: re.Match) -> bool:
        opening_hours = self._opening_hours
        if opening_hours[date.group('day')]:
            int_hour = hour_int(date.group('hour'))
            time_min = time_slot_int(opening_hours[date.group('day')][0])[0]
            time_max = time_slot_int(opening_hours[date.group('day')][-1])[-1]
            if time_min <= int_hour <= time_max:
                return True

        return False

    def in_rush_hour(self, date: re.Match) -> bool:
        # TODO: gestion des heures +1/-1 incorrectes sur des horaires proches de minuit
        opening_hours = self._opening_hours

        if not opening_hours or date.group('day') not in opening_hours or\
                not opening_hours[date.group('day')] or\
                self.is_always_open:
            return False
        int_hour = hour_int(date.group('hour'))
        time_min = time_slot_int(opening_hours[date.group('day')][0])[0]
        time_max = time_slot_int(opening_hours[date.group('day')][-1])[-1]

        if time_min == 0 and time_max == 24:  # 24/7
            return False
        elif time_min - 1 < int_hour <= time_min + 1 or \
                time_max - 1 <= int_hour < time_max + 1:
            return True
        elif self.landuse == 'residential' and\
                (time_min - 1 <= int_hour <= time_min + 2 or
                 time_max - 2 <= int_hour <= time_max + 1):
            return True

        return False

    def coef_rush(self, date: re.Match) -> float:
        if self.in_rush_hour(date):
            if self.landuse == "residential" or self.is_school_building:
                return 1
            return 0.25
        if self.is_open(date):
            if self.shop == 'supermarket' or self.amenity == 'marketplace':
                return 0.15
            elif self.is_always_open:
                return 0.1
            return 0.05

        return int(self.is_open_or_on_break(date))*0.05

    @property
    def is_school_building(self) -> bool:
        return self.amenity in ('school', 'college', 'kindergarten', 'childcare')

    @property
    def is_always_open(self) -> bool:
        return self.amenity in ('police', 'fire_station', 'hospital', 'place_of_worship')

    class Meta:
        verbose_name = "noeud"
        ordering = ['id']


def influencers_queryset() -> QuerySet:
    return Node.objects.filter(is_influencer=True)


def conflicts_queryset() -> QuerySet:
    return Node.objects.filter(is_conflict=True)


ROOT_IMG = 'static/img/'


class City(models.Model):
    id = models.IntegerField(primary_key=True)
    position = models.PointField(default=Point(0, 0))
    name = models.CharField(max_length=255, default="")
    postal_code = models.IntegerField()
    img_file = models.CharField(max_length=255, default="")
    nb_click = models.IntegerField(default=0)

    def load(self, **kwargs):
        new_attrs = dict(**kwargs.get('tags', {}), **kwargs)
        new_attrs['position'] = Point(kwargs['lat'], kwargs['lon'])

        root_img = ROOT_IMG + str(kwargs['postal_code']) + '_apercu.png'
        if not os.path.exists(os.path.join(BASE_DIR, root_img)):
            root_img = ""
        new_attrs['img_file'] = root_img

        for k, v in new_attrs.items():
            setattr(self, k, v)

    class Meta:
        ordering = ['-nb_click']