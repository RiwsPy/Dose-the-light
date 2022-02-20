# Generated by Django 4.0.1 on 2022-01-16 08:36

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0, 0), srid=4326)),
                ('is_conflict', models.BooleanField(default=True)),
                ('is_influencer', models.BooleanField(default=False)),
                ('conflicts_value', models.IntegerField(default=0)),
                ('conflicts_details', models.TextField(default='')),
                ('opening_hours', models.CharField(default='', max_length=255)),
                ('name', models.CharField(default='', max_length=255)),
                ('amenity', models.CharField(default='', max_length=255)),
                ('highway', models.CharField(default='', max_length=255)),
                ('shop', models.CharField(default='', max_length=255)),
                ('landuse', models.CharField(default='', max_length=255)),
                ('public_transport', models.CharField(default='', max_length=255)),
                ('bus', models.CharField(default='', max_length=255)),
                ('railway', models.CharField(default='', max_length=255)),
                ('details', models.CharField(default='', max_length=255)),
            ],
        ),
    ]