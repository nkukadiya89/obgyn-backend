# Generated by Django 3.2.9 on 2022-05-06 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_fields', '0004_auto_20220117_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='managefieldsmodel',
            name='field_value',
            field=models.CharField(default='', max_length=500),
        ),
    ]