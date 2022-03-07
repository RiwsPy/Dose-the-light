from django.test import TestCase
from maps.models import Node
from django.contrib.gis.geos import Point
import json


class Test_Node(TestCase):
    def setUp(self):
        node_01 = Node.objects.create(
            id=1)
        Node.objects.create(
            id=2,
            opening_hours='Mo 08:00-20:00'
        )

    def test_pr_dict(self):
        node = Node.objects.get(pk=1)
        self.assertEqual(node.pr_dict,
                         {
                          'type': 'Feature',
                          'geometry': {
                              'coordinates': [0.0, 0.0],
                              'type': 'Point'
                            },
                          'properties': {
                              'amenity': '',
                              'bus': '',
                              'conflicts_details': '',
                              'conflicts_value': 0,
                              'details': '',
                              'highway': '',
                              'id': 1,
                              'is_conflict': True,
                              'is_influencer': False,
                              'landuse': '',
                              'name': '',
                              'opening_hours': '',
                              'public_transport': '',
                              'railway': '',
                              'shop': ''
                            }})
