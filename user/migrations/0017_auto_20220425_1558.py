# Generated by Django 3.2.9 on 2022-04-25 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_auto_20220416_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='operative_charge',
        ),
        migrations.RemoveField(
            model_name='user',
            name='rs_per_day_nursing',
        ),
        migrations.RemoveField(
            model_name='user',
            name='rs_per_room',
        ),
        migrations.RemoveField(
            model_name='user',
            name='rs_per_usg',
        ),
        migrations.RemoveField(
            model_name='user',
            name='rs_per_visit',
        ),
    ]
