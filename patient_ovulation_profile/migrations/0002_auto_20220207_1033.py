# Generated by Django 3.2.9 on 2022-02-07 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_ovulation_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientovulationprofilemodel',
            name='day',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='patientovulationprofilemodel',
            name='endometrium_mm',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='patientovulationprofilemodel',
            name='left_ovary_mm',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='patientovulationprofilemodel',
            name='op_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='patientovulationprofilemodel',
            name='ovarian_blood_flow',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='patientovulationprofilemodel',
            name='remark',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='patientovulationprofilemodel',
            name='right_ovary_mm',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='patientovulationprofilemodel',
            name='ut_blood_flow',
            field=models.CharField(default='', max_length=100),
        ),
    ]
