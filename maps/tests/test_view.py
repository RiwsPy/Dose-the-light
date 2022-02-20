import django
from django.test import TestCase
import json
from pathlib import Path
import os
from django.conf import settings
settings.configure()
django.setup()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

"""
class HomePage(TestCase):
    def test_show_json(self):
        response = self.client.get('http://127.0.0.1:5000/maps/api/monday.json')
        with open(os.path.join(BASE_DIR, 'db/monday.json'), 'r') as file:
            assert json.load(file) == response.json()
"""