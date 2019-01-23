from django.test import TestCase
from django.core.management import call_command


class PopulateHouseholdsTest(TestCase):
    def test_raise_value_error(self):
        self.assertRaises(
            ValueError,
            lambda: call_command('populate_households', country_code='abc')
        )
