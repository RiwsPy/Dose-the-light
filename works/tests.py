from django.test import TestCase
from works import Works


class Test_basic_works(TestCase):
    def test_create(self):
        w = Works()

        self.assertEqual(w.features, [])


class Test_avanced_works(TestCase):

    def test_un(self):
        w = Works()
        w.load('base')
        self.assertEqual(len(w), 3)
        self.assertEqual(w.filename, '38170_empty')
