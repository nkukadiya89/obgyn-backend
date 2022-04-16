# Generated by Django 3.2.9 on 2022-04-14 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0006_alter_timingmodel_timing'),
        ('diagnosis', '0009_diagnosismodel_diagnosis_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosismodel',
            name='medicine',
            field=models.ManyToManyField(blank=True, to='medicine.MedicineModel'),
        ),
    ]