# Generated by Django 3.2.9 on 2022-06-02 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('obgyn_config', '0013_auto_20220602_1611'),
    ]

    operations = [
        migrations.RenameField(
            model_name='obgynconfigmodel',
            old_name='manage_field',
            new_name='prefix',
        ),
    ]
