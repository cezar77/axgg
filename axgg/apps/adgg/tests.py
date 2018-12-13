from datetime import date

from django.test import TestCase
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

from .constants import NAME_SCHEMA
from .validators import JsonSchemaValidator
from .models import Person


#class JsonSchemaValidatorTest(SimpleTestCase):
#    TEST_DATA = [
#        (
#            JsonSchemaValidator(limit_value=NAME_SCHEMA),
#            {'first': 'Max', 'last': 'Mustermann'},
#            None
#        ),
#        (
#            JsonSchemaValidator(limit_value=NAME_SCHEMA),
#            {'first': 'Cezar', 'middle': 'Kimani', 'last': 'Pendarovski'},
#            None
#        ),
#        (
#            JsonSchemaValidator(limit_value=NAME_SCHEMA),
#            {'first': 1, 'middle': None, 'last': 2},
#            ValidationError
#        ),
#        (
#            JsonSchemaValidator(limit_value=NAME_SCHEMA),
#            {'first_name': 'Max', 'surname': 'Mustermann'},
#            ValidationError
#        )
#    ]
#
#    def test_validator(self):
#        for validator, value, expected in self.TEST_DATA:
#            name = validator.__class__.__name__
#            exception = expected is not None and issubclass(expected, Exception)
#            with self.subTest(name, value=value):
#                if exception:
#                    with self.assertRaises(expected):
#                        validator(value)
#                else:
#                    self.assertEqual(expected, validator(value))


class PersonTest(TestCase):
    def setUp(self):
        self.p = Person(
            name={'first': 'Max', 'last': 'Mustermann'},
            language='sw',
            sex='M',
            birthdate=date(1980, 1, 1),
            phone='123456789',
            roles=['F'],
        )

    def test_name_contains_only_required_keys(self):
        self.p.save()
        self.assertEqual({'first': 'Max', 'last': 'Mustermann'}, self.p.name)

    def test_name_contains_all_keys(self):
        self.p.name = {'first': 'Cezar', 'middle': 'Kimani', 'last': 'Pendarovski'}
        self.p.save()
        self.assertEqual({'first': 'Cezar', 'middle': 'Kimani', 'last': 'Pendarovski'}, self.p.name)

    def test_name_contains_invalid_key(self):
        self.p.name = {'first': 'Max', 'second': 'F', 'last': 'Mustermann'}
        self.assertRaises(ValidationError, self.p.full_clean())

    def test_name_contains_invalid_value(self):
        self.p.name = {'first': 1, 'middle': None, 'last': True}
        self.assertRaises(ValidationError, self.p.full_clean())

    def test_full_name_with_only_required_keys(self):
        self.p.save()
        self.assertEqual('Max Mustermann', self.p.full_name)

    def test_full_name_with_all_keys(self):
        self.p.name = {'first': 'Cezar', 'middle': 'Kimani', 'last': 'Pendarovski'}
        self.p.save()
        self.assertEqual('Cezar Kimani Pendarovski', self.p.full_name)
