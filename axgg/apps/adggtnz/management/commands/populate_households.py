import os
import json
import re
import argparse

import iso8601

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point

from axgg.apps.adgg.models import Country
from axgg.apps.adgg.models import Household
from axgg.apps.adgg.models import FarmPerson
from axgg.apps.adgg.models import Log


def country_iso_code(string):
    value = string.upper()
    if not re.match('^[A-Z]{2}$', value):
        raise argparse.ArgumentError()
    return value


class Command(BaseCommand):
    help = ('Populate the households database table with values parsed'
            ' from JSON files.')

    def add_arguments(self, parser):
        parser.add_argument(
            'source_dir',
            type=str,
            help='The source directory with the JSON files.'
        )
        parser.add_argument(
            '--country_code',
            type=country_iso_code,
            default='TZ',
            help='The 2-digit ISO code of the country'
        )
        parser.add_argument(
            '--paid',
            action='store_true',
            default=False,
            help='Specify if the surveys are from a PAID project'
        )

    def handle(self, *args, **options):
        """
        Open the directory containing the JSON files and iterate over
        them.
        """
        source_dir = options['source_dir']
        country_code = options['country_code']
        country = Country.objects.get(id=country_code)
        paid = options['paid']
        for filename in os.listdir(source_dir):
            self.stdout.write(
                self.style.NOTICE(
                    'File {} is processed.'.format(filename)
                )
            )
            with open(os.path.join(source_dir, filename)) as jsonfile:
                try:
                    result = json.load(jsonfile)
                except json.decoder.JSONDecodeError:
                    self.stdout.write(
                        self.style.ERROR(
                            'The file {} is not a valid JSON format.'.format(filename)
                        )
                    )
                    result = None
            if result:
                self.run(result, country, paid)

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
        gps_data = value.split(' ')
        pnt = [float(gps_data[1]), float(gps_data[0])]
        return {
            'geolocation': pnt,
            'altitude': round(float(gps_data[2])),
            'hdop': float(gps_data[3])
        }

    def transform_end_time(self, value):
        """
        Use the end_time of the survey as registration date, since we
        need a datetime object.
        """
        return iso8601.parse_date(value)

    def transform_name(self, value):
        """
        Extract first, middle and last name from name.
        """
        if value is None:
            return ('', '', '')
        name = re.sub(r'\(.*?\)', '', value)
        name = name.replace('.', ' ')
        name = name.replace('  ', ' ')
        name_parts = name.split(' ')
        if not len(name_parts):
            return ('', '', '')
        first_name = name_parts[0].capitalize()
        last_name = name_parts[len(name_parts)-1].capitalize()
        middle_name = ' '.join(name_parts[1:len(name_parts)-1]).capitalize()
        return first_name, middle_name, last_name

    def transform_gender(self, value):
        if value == '1':
            return 'M'
        elif value == '2':
            return 'F'

    def transform_is_household_head(self, value):
        if value == '0':
            return False
        elif value == '1':
            return True

    def check_farm_is_registered(self, result):
        farm_registered = result.get('farmregistered', None)
        if farm_registered == '1' or farm_registered is None:
            self.stdout.write(
                self.style.WARNING(
                    'This farmer has already been registered.'
                )
            )
            return True
        return False

    def run(self, result, country, paid):
        if paid:
            if self.check_farm_is_registered(result):
                return

        registration_date = self.transform_end_time(result['end_time'])
        uuid = result['_uuid']

        gpsloc = result.get('grpfarmreg/gpsloc', False) or result.get('gpsloc', False)
        if not gpsloc:
            Log.objects.create(uuid=uuid, comment='There is no data for geolocation')
            self.stdout.write(
                self.style.NOTICE(
                    'The file with UUID {} has been logged.'.format(uuid)
                )
            )
            return
        gps_data = self.transform_gpsloc(gpsloc)

        farmer_name = self.transform_name(result.get('farmerdetails/farmername'))
        farmer_phone = result.get('farmerdetails/farmermobile')
        farmer_gender = self.transform_gender(result.get('farmerdetails/farmergender'))
        farmer_hhhead = self.transform_is_household_head(result.get('farmerdetails/farrmerhhhead'))

        farmer = head =FarmPerson(
            first_name=farmer_name[0],
            middle_name=farmer_name[1],
            last_name=farmer_name[2],
            language='SW',
            sex=farmer_gender,
            phone=farmer_phone
        )

        if farmer_hhhead == False:
            head_name = self.transform_name(result.get('hhheaddetails/hhhname'))
            head_phone = result.get('hhheaddetails/hhhmobile')
            head_gender = self.transform_gender(result.get('hhheaddetails/hhhgender'))
            head = FarmPerson(
                first_name=head_name[0],
                middle_name=head_name[1],
                last_name=head_name[2],
                language='SW',
                sex=head_gender,
                phone=head_phone
            )
        print(head)

        feedback_members = []
        for member in result.get('rpt_b_membrs'):
            member_name = self.transform_name(member.get('rpt_b_membrs/rpt_b_membrs_layout/name'))
            member_phone = member.get('rpt_b_membrs/rpt_b_membrs_layout/mobile')
            member_gender = self.transform_gender(member.get('rpt_b_membrs/rpt_b_membrs_layout/gender'))
            feedback_member = FarmPerson(
                first_name=member_name[0],
                middle_name=member_name[1],
                last_name=member_name[2],
                language='SW',
                sex=member_gender,
                phone=member_phone
            )
            feedback_members.append(feedback_member)

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
                geolocation=Point(gps_data['geolocation']),
                altitude=gps_data['altitude'],
                hdop=gps_data['hdop'],
                country=country,
                registration_date=registration_date,
                active=True,
                uuid=uuid,
                farmer=farmer,
                head=head,
                feedback_members=feedback_members
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
