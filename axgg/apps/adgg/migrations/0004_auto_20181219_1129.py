# Generated by Django 2.1.4 on 2018-12-19 11:29

import axgg.apps.adgg.models
import django.contrib.postgres.fields
from django.db import migrations

from  ..models import FarmPerson

class Migration(migrations.Migration):

    dependencies = [
        ('adgg', '0003_auto_20181214_0924'),
    ]

    operations = [
        FarmPerson.Operation(),
        migrations.AddField(
            model_name='household',
            name='farmer',
            field=FarmPerson.Field(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='household',
            name='feedback_members',
            field=django.contrib.postgres.fields.ArrayField(FarmPerson.Field(), default=None, size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='household',
            name='head',
            field=FarmPerson.Field(default=None),
            preserve_default=False,
        ),
    ]