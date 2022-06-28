# Generated by Django 3.2.9 on 2022-06-27 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_delivery', '0012_patientdeliverymodel_lastname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdeliverymodel',
            name='delivery_type',
            field=models.CharField(choices=[('NORMAL', 'NORMAL'), ('CESARIAN', 'CESARIAN'), ('INSTRUMENTAL', 'INSTRUMENTAL')], default='NORMAL', max_length=20),
        ),
    ]