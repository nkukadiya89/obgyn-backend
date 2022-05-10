# Generated by Django 3.2.9 on 2022-05-10 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_fields', '0005_alter_managefieldsmodel_field_value'),
        ('patient_indoor', '0006_remove_patientindoormodel_field_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientindoormodel',
            name='provisional_diagnosis',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='provisional_diagnosis', to='manage_fields.managefieldsmodel'),
        ),
    ]