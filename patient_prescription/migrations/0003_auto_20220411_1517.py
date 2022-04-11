# Generated by Django 3.2.9 on 2022-04-11 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0006_alter_timingmodel_timing'),
        ('patient_prescription', '0002_patientprescriptionmodel_patient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientprescriptionmodel',
            name='diagnosis',
        ),
        migrations.AddField(
            model_name='patientprescriptionmodel',
            name='medicine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='medicine.medicinemodel'),
        ),
    ]
