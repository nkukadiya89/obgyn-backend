# Generated by Django 3.2.9 on 2022-05-06 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0013_patientmodel_first_edd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientmodel',
            name='department',
        ),
        migrations.RemoveField(
            model_name='patientmodel',
            name='patient_detail',
        ),
        migrations.RemoveField(
            model_name='patientmodel',
            name='patient_type',
        ),
    ]
