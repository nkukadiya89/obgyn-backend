# Generated by Django 3.2.9 on 2022-03-02 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_billing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientbillingmodel',
            name='admission_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='patientbillingmodel',
            name='discharge_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='patientbillingmodel',
            name='ot_date',
            field=models.DateTimeField(null=True),
        ),
    ]
