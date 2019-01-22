# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ViewAllfarmers(models.Model):
    regdate = models.DateTimeField(blank=True, null=True)
    hh_country = models.IntegerField(blank=True, null=True)
    hh_region = models.CharField(max_length=11, blank=True, null=True)
    hh_district = models.CharField(max_length=11, blank=True, null=True)
    hh_kebele = models.CharField(max_length=11, blank=True, null=True)
    hh_village = models.CharField(max_length=11, blank=True, null=True)
    aitechid = models.CharField(max_length=60, blank=True, null=True)
    farmername = models.TextField(blank=True, null=True)
    farmermobile = models.CharField(max_length=60, blank=True, null=True)
    farmergender = models.IntegerField(blank=True, null=True)
    cattletotalowned = models.IntegerField(blank=True, null=True)
    gpsloc = models.CharField(max_length=150, blank=True, null=True)
    rowuuid = models.CharField(primary_key=True, max_length=80)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'view_allfarmers'
