# Generated by Django 3.2.9 on 2022-06-02 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_fields', '0006_fieldmastermodel_slug'),
        ('obgyn_config', '0014_rename_manage_field_obgynconfigmodel_prefix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obgynconfigmodel',
            name='prefix',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='config_prefix', to='manage_fields.managefieldsmodel'),
        ),
    ]