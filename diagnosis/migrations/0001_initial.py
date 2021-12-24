# Generated by Django 3.2.9 on 2021-12-07 11:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medicine', '0002_auto_20211207_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiagnosisModel',
            fields=[
                ('diagnosis_id', models.AutoField(primary_key=True, serialize=False)),
                ('diagnosis_name', models.CharField(default='', max_length=150)),
                ('created_by', models.IntegerField(default=1)),
                ('deleted', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('medicine', models.ManyToManyField(to='medicine.MedicineModel')),
            ],
            options={
                'db_table': 'diagnosis',
            },
        ),
    ]