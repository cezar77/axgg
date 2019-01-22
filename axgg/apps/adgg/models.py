from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.functional import cached_property


class Household(models.Model):
    geolocation = models.PointField(blank=True, null=True)
    altitude = models.SmallIntegerField(blank=True, null=True)
    hdop = models.FloatField(verbose_name='Horizontal dilution of precision', blank=True, null=True)
    country = models.CharField(max_length=3)
    registration_date = models.DateTimeField()
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField()
    uuid = models.CharField(max_length=100)
    properties = JSONField(blank=True, null=True)

    def __str__(self):
        return '{} from {}'.format(
            self.uuid,
            self.registration_date.strftime('%d %B %Y')
        )

    @cached_property
    def longitude(self):
        if self.geolocation:
            return self.geolocation.x
        return None

    @cached_property
    def latitude(self):
        if self.geolocation:
            return self.geolocation.y
        return None
