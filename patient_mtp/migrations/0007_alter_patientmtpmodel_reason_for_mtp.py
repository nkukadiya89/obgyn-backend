# Generated by Django 3.2.9 on 2022-05-18 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_mtp', '0006_auto_20220315_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientmtpmodel',
            name='reason_for_mtp',
            field=models.CharField(max_length=250, null=True),
        ),
    ]