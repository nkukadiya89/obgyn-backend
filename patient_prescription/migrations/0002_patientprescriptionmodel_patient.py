# Generated by Django 3.2.9 on 2022-01-24 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_remove_patientmodel_pid'),
        ('patient_prescription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientprescriptionmodel',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patient.patientmodel'),
        ),
    ]