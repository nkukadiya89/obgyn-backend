# Generated by Django 3.2.9 on 2022-01-31 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surgical_item', '0006_rename_drug_name_surgicalitemgroupmodel_drug_group_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surgicalitemmodel',
            name='exp_date',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='surgicalitemmodel',
            name='mfg_date',
            field=models.CharField(default='', max_length=25),
        ),
    ]