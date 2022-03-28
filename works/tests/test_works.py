from django.test import TestCase
from works import Works


class Test_works(TestCase):
    def setUp(self):
        pass
        #w = Works()

    def test_create(self):
        w = Works()

        self.assertEqual(w.features, [])
