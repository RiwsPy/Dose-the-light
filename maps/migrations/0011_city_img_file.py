# Generated by Django 4.0.1 on 2022-03-18 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0010_alter_city_postal_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='img_file',
            field=models.CharField(default='', max_length=255),
        ),
    ]
