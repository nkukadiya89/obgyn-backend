# Generated by Django 3.2.9 on 2022-06-02 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_fields', '0006_fieldmastermodel_slug'),
        ('obgyn_config', '0012_auto_20220530_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='obgynconfigmodel',
            name='field_master_name',
        ),
        migrations.AddField(
            model_name='obgynconfigmodel',
            name='manage_field',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='manage_fields.managefieldsmodel'),
        ),
    ]