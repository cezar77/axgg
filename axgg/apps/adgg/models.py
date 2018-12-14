from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.db import models
from django.utils.functional import cached_property
  
from .constants import *
from .validators import JsonSchemaValidator


class Country(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=60)
    iso3 = models.CharField(max_length=3, unique=True)
    num_code = models.PositiveSmallIntegerField(null=True, blank=True)
    phone_code = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class Household(models.Model):
    geolocation = models.PointField()
    altitude = models.SmallIntegerField()
    hdop = models.FloatField(verbose_name='Horizontal dilution of precision')
    country = models.ForeignKey(
        'Country',
        related_name='households',
        on_delete=models.DO_NOTHING
    )
    registration_date = models.DateTimeField()
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField()
    uuid = models.CharField(max_length=100)

    def __str__(self):
        return '{} from {}'.format(
            self.uuid,
            self.registration_date.strftime('%d %B %Y')
        )

    @cached_property
    def longitude(self):
        return self.geolocation.x

    @cached_property
    def latitude(self):
        return self.geolocation.y


class Person(models.Model):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    sex = models.CharField(max_length=1, choices=SEXES)
    birthdate = JSONField(
        default=dict,
        validators=[JsonSchemaValidator(limit_value=DATE_SCHEMA)]
    )
    phone = models.CharField(max_length=20)
    roles = ArrayField(models.CharField(max_length=1, choices=ROLES))
    email = models.EmailField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    organisation = models.CharField(max_length=50, blank=True)
    household = models.ForeignKey(
        'Household',
        related_name='people',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    class Meta:
        verbose_name_plural = 'People'

    @cached_property
    def full_name(self):
        name_parts = [self.first_name, self.last_name]
        if self.middle_name:
            name_parts.insert(1, self.middle_name)
        return ' '.join(name_parts)


class Log(models.Model):
    uuid = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=STATUS, default='NEW')
