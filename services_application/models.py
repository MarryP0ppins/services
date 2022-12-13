# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Contract(models.Model):
    id = models.IntegerField(primary_key=True)
    client = models.ForeignKey('User', models.DO_NOTHING)
    service = models.ForeignKey('Service', models.DO_NOTHING)
    date_of_execution = models.DateTimeField()
    date_of_signing = models.DateTimeField()
    status = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'contract'


class Service(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    title = models.CharField(max_length=45)
    duration = models.DateField()
    price = models.FloatField()
    rating = models.IntegerField()
    city = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'service'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    sex = models.CharField(max_length=6)
    phone = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45)
    date_of_registration = models.DateTimeField()
    date_of_birth = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user'
