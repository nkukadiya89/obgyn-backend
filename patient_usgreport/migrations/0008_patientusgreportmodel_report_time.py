# Generated by Django 3.2.9 on 2022-07-08 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_usgreport', '0007_alter_patientusgreportmodel_patient_opd'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientusgreportmodel',
            name='report_time',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
