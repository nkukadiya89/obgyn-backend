# Generated by Django 3.2.9 on 2022-03-11 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_mtp', '0002_alter_patientmtpmodel_reason_for_mtp'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientmtpmodel',
            name='termination_date',
            field=models.DateField(null=True),
        ),
    ]
