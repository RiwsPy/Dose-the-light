# Generated by Django 4.0.1 on 2022-03-18 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0008_alter_city_postal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='postal_code',
            field=models.IntegerField(unique=True),
        ),
    ]
