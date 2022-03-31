# Generated by Django 3.2.9 on 2022-03-22 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_fields', '0004_auto_20220117_1601'),
        ('patient_indoor', '0002_alter_patientindoormodel_temprature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientindoormodel',
            name='eb_pp',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='eb_pp_indr', to='manage_fields.managefieldsmodel'),
        ),
        migrations.AlterField(
            model_name='patientindoormodel',
            name='operation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='operation_indr', to='manage_fields.managefieldsmodel'),
        ),
        migrations.AlterField(
            model_name='patientindoormodel',
            name='ps',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ps_indr', to='manage_fields.managefieldsmodel'),
        ),
        migrations.AlterField(
            model_name='patientindoormodel',
            name='pv',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pv_indr', to='manage_fields.managefieldsmodel'),
        ),
    ]