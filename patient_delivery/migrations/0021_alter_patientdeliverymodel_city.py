# Generated by Django 3.2.9 on 2023-03-31 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_delivery', '0020_auto_20230329_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdeliverymodel',
            name='city',
            field=models.CharField(max_length=55, null=True),
        ),
    ]
