# Generated by Django 3.2.9 on 2022-03-14 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_billing', '0005_auto_20220314_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientbillingmodel',
            name='ot_time',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
