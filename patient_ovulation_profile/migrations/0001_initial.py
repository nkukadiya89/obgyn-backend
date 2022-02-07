# Generated by Django 3.2.9 on 2022-02-05 14:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patient', '0007_rename_husband_name_patientmodel_husband_father_name'),
        ('patient_opd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientOvulationProfileModel',
            fields=[
                ('patient_ovulation_profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('regd_no', models.CharField(default='', max_length=100)),
                ('created_by', models.IntegerField(default=1)),
                ('deleted', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='patient.patientmodel')),
                ('patient_opd', models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patient_opd.patientopdmodel')),
            ],
            options={
                'db_table': 'patient_ovulation_profile',
            },
        ),
    ]
