# Generated by Django 4.0.1 on 2022-03-18 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0005_city_alter_node_options_delete_conflictsinrange'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='nb_click',
            field=models.IntegerField(default=0),
        ),
    ]