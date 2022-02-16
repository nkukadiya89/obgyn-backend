# Generated by Django 3.2.9 on 2022-02-16 10:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patient', '0010_patientmodel_name_title'),
        ('patient_opd', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientMtpModel',
            fields=[
                ('patient_mtp_id', models.AutoField(primary_key=True, serialize=False)),
                ('regd_no', models.CharField(default='', max_length=100)),
                ('second_rmp', models.CharField(max_length=25, null=True)),
                ('reason_for_mtp', models.TextField(null=True)),
                ('contraception', models.CharField(max_length=100, null=True)),
                ('mtp_complication', models.CharField(max_length=500, null=True)),
                ('discharge_date', models.DateField(null=True)),
                ('remark', models.TextField(null=True)),
                ('created_by', models.IntegerField(default=1)),
                ('deleted', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='patient.patientmodel')),
                ('patient_opd', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='patient_opd.patientopdmodel')),
            ],
            options={
                'db_table': 'patient_mtp',
            },
        ),
    ]
