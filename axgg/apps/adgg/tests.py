from io import StringIO

from django.test import TestCase
from django.core.management import call_command


class PopulateHouseholdsTest(TestCase):
    def test_raise_value_error(self):
        out = StringIO()
        call_command('populate_households', stdin='abc', stdout=out)
        self.assertRaises(ValueError, out.getValue())
