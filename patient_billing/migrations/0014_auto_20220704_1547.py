# Generated by Django 3.2.9 on 2022-07-04 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_fields', '0006_fieldmastermodel_slug'),
        ('patient_billing', '0013_patientbillingmodel_invoice_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientbillingmodel',
            name='other_charge',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='billing_other_charge', to='manage_fields.managefieldsmodel'),
        ),
        migrations.AlterField(
            model_name='patientbillingmodel',
            name='room_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='billing_room_type', to='manage_fields.managefieldsmodel'),
        ),
    ]