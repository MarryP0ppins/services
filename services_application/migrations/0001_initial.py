# Generated by Django 4.1.4 on 2022-12-13 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date_of_execution', models.DateTimeField()),
                ('date_of_signing', models.DateTimeField()),
                ('status', models.CharField(max_length=11)),
            ],
            options={
                'db_table': 'contract',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=45)),
                ('duration', models.DateField()),
                ('price', models.FloatField()),
                ('rating', models.IntegerField()),
                ('city', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'service',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('sex', models.CharField(max_length=6)),
                ('phone', models.CharField(blank=True, max_length=45, null=True)),
                ('email', models.CharField(max_length=45)),
                ('date_of_registration', models.DateTimeField()),
                ('date_of_birth', models.DateTimeField()),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
    ]