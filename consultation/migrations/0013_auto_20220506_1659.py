# Generated by Django 3.2.9 on 2022-05-06 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0012_auto_20220416_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultationmodel',
            name='department',
            field=models.CharField(choices=[('OPD', 'OPD'), ('IPD', 'IPD')], default='OPD', max_length=5),
        ),
        migrations.AddField(
            model_name='consultationmodel',
            name='patient_detail',
            field=models.CharField(choices=[('FULL', 'FULL'), ('PARTIAL', 'PARTIAL')], default='PARTIAL', max_length=8),
        ),
        migrations.AddField(
            model_name='consultationmodel',
            name='patient_type',
            field=models.CharField(choices=[('OB', 'OB'), ('GYN', 'GYN')], default='OB', max_length=5),
        ),
    ]