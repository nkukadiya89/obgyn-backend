# Generated by Django 3.2.9 on 2022-01-18 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0004_auto_20211228_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnosisMedicineModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'diagnosis_medicine',
                'managed': False,
            },
        ),
    ]