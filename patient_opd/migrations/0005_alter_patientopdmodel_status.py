# Generated by Django 3.2.9 on 2022-03-30 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient_opd', '0004_patientopdmodel_opd_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientopdmodel',
            name='status',
            field=models.CharField(max_length=25, null=True),
        ),
    ]