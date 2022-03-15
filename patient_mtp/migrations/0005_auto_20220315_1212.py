# Generated by Django 3.2.9 on 2022-03-15 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_mtp', '0004_patientmtpmodel_discharge_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientmtpmodel',
            name='admission_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='patientmtpmodel',
            name='admission_time',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='patientmtpmodel',
            name='procedure_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='patientmtpmodel',
            name='procedure_time',
            field=models.CharField(max_length=10, null=True),
        ),
    ]