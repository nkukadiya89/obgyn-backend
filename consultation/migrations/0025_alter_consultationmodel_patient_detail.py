# Generated by Django 3.2.9 on 2022-07-11 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0024_alter_consultationmodel_patient_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultationmodel',
            name='patient_detail',
            field=models.CharField(choices=[('FULL', 'FULL'), ('PARTIAL', 'PARTIAL')], max_length=8, null=True),
        ),
    ]
