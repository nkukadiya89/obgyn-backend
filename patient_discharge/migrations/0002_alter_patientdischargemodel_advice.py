# Generated by Django 3.2.9 on 2022-02-27 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_fields', '0004_auto_20220117_1601'),
        ('patient_discharge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientdischargemodel',
            name='advice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='manage_fields.managefieldsmodel'),
        ),
    ]