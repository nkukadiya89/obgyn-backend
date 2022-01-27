# Generated by Django 3.2.9 on 2022-01-26 11:17

import django.utils.timezone
from django.db import migrations, models

from manage_fields.models import ManageFieldsModel, FieldMasterModel


def load_data(apps, edit_schema):
    master_field = FieldMasterModel.objects.create(field_master_name="Indication/S for Diagnostics Procedure")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="Evaluation of foetal-growth parameters,weight wellbeing")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="Any suspected adenexal or uterine pathology/abnormality")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="Assessment of cervical canal and diameter of internal os")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field, field_value="Assessment of liquor amnii")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="Detection of number of foctuses and their chorionicity")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="Detection of chromosomal abnormalities foetal structural defects other abnormalities their follow-up")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="Discrepancy between uterine size and period of amenorrhoea")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="Estimation of gestational age(dating)")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="Evaluation of placental Position,thickness,grading abnormalities(placenta pracvia,retroplacental haemorrhage,abnormal adherence etc.)")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="Evaluation of umbilical cord-presentation,insertion,nuchal encirclement,number of vessels and presence of true knot")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="Follow up of cases of abortion")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="Medical/surgical conditions complicating pregnancy")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="Preterm labour/preterm premature rupture of membrances")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="Suspected pregnancy with IUCD in-situ or suspected pregnancy following contraceptive failure/MTP failure")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="To diagnose intra-uterine and/or ectopic pregnancy and confirm viability")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field,
                                     field_value="To evalute foetal presentation and position")
    ManageFieldsModel.objects.create(language_id=1, field_master=master_field, field_value="Vaginal bleeding/leaking")


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('manage_fields', '0004_auto_20220117_1601'),
        ('patient', '0004_remove_patientmodel_pid'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientReferalModel',
            fields=[
                ('patient_referal_id', models.AutoField(primary_key=True, serialize=False)),
                ('regd_no', models.CharField(default='', max_length=100)),
                ('created_by', models.IntegerField(default=1)),
                ('deleted', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('indication', models.ManyToManyField(to='manage_fields.ManageFieldsModel')),
                ('patient',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='patient.patientmodel')),
            ],
            options={
                'db_table': 'patient_referal',
            },
        ),
        migrations.RunPython(load_data)
    ]