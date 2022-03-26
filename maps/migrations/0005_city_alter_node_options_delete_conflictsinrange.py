# Generated by Django 4.0.1 on 2022-03-18 07:26

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0004_alter_conflictsinrange_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('position', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0, 0), srid=4326)),
                ('name', models.CharField(default='', max_length=255)),
                ('postal_code', models.IntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='node',
            options={'ordering': ['id'], 'verbose_name': 'noeud'},
        ),
        migrations.DeleteModel(
            name='ConflictsInRange',
        ),
    ]