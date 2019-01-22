import argparse
import re

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from axgg.apps.adgg.models import Household
from axgg.apps.adggtnz.models import ViewAllfarmers


def country_iso_code(string):
    value = string.lower()
    if not re.match('^[a-z]{3}$', value):
        raise argparse.ArgumentError()
    return value


class Command(BaseCommand):
    help = ('Populate the households database table with values parsed'
            ' from the old database.')

    def add_arguments(self, parser):
        parser.add_argument(
            '--country_code',
            type=country_iso_code,
            default='tnz',
            help='The 3-digit ISO code of the country'
        )

    def handle(self, *args, **options):
        """
        Read the data from the old database, transform it and insert
        it into the new database.
        """
        country = options['country_code']
        qs = ViewAllfarmers.objects.all()
        print(qs.count())
        for item in qs:
            registration_date = item.regdate
            geolocation, altitude, hdop = self.transform_gpsloc(item.gpsloc)
            uuid = item.rowuuid
            try:
                # check if a household object exists
                Household.objects.get(
                    registration_date=registration_date,
                    uuid=uuid
                )
                self.stdout.write(
                    self.style.WARNING(
                        'Household entry with uuid {} already exists!'.format(uuid)
                    )
                )
            except Household.DoesNotExist:
                # persist a household object into the DB
                Household.objects.create(
                    geolocation=Point(geolocation),
                    altitude=altitude,
                    hdop=hdop,
                    country=country,
                    registration_date=registration_date,
                    active=True,
                    uuid=uuid,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        'Household entry with uuid {} successfully created.'.format(uuid)
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        'An unexpected error occured {}.'.format(e.__class__.__name__)
                    )
                )

    def transform_gpsloc(self, value):
        """
        Transform the value for gsploc into a point, altitude and hdop.
        The point consist of the first value (longitude) in the string
        and of the second value (latitude) in the string.
        The altitude is the third value in the string. We round the
        altitude to the nearest integer.
        The horizontal dilution of precision is the fourth value in the
        string.
        """
        if value is not None:
            gps_data = value.split(' ')
            geolocation = self.get_geolocation(gps_data[0], gps_data[1])
            altitude = self.get_altitude(gps_data[2])
            hdop = self.get_hdop(gps_data[3])
            pnt = [float(gps_data[1]), float(gps_data[0])]
            return (geolocation, altitude, hdop)
        return ([], None, None)

    @staticmethod
    def get_geolocation(lon, lat):
        longitude = round(float(lon), 2)
        latitude = round(float(lat), 2)
        return [latitude, longitude]

    @staticmethod
    def get_altitude(altitude):
        return int(float(altitude))

    @staticmethod
    def get_hdop(hdop):
        return round(float(hdop), 1)
