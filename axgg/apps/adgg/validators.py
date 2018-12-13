from cerberus import Validator

from django.core.validators import BaseValidator


class JsonSchemaValidator(BaseValidator):
    def compare(self, a, b):
        v = Validator(b)
        return v.validate(a)
