# Generated by Django 3.2.9 on 2022-05-27 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient_delivery', '0003_auto_20220411_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patientdeliverymodel',
            old_name='father_eduction',
            new_name='father_education',
        ),
    ]