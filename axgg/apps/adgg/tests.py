from django.test import TestCase

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
            first_name='Max',
            last_name='Mustermann',
            language='sw',
            sex='M',
            birthdate={'day': 1, 'month': 1, 'year': 1980},
            phone='123456789',
            roles=['F'],
        )

    def test_full_name_without_middle_name(self):
        self.p.save()
        self.assertEqual('Max Mustermann', self.p.full_name)

    def test_full_name_with_middle_name(self):
        self.p.middle_name = 'Kimani'
        self.p.save()
        self.assertEqual('Max Kimani Mustermann', self.p.full_name)
