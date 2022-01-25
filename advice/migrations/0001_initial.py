# Generated by Django 3.2.9 on 2022-01-18 07:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdviceModel',
            fields=[
                ('advice_id', models.AutoField(primary_key=True, serialize=False)),
                ('advice', models.TextField(null=True)),
                ('advice_for', models.CharField(choices=[('OPD', 'OPD'), ('SONOGRAPHY', 'SONOGRAPHY'), ('GENERAL', 'GENERAL'), ('POST-CS', 'POST-CS'), ('PRE-CS', 'PRE-CS')], default='OPD', max_length=15)),
                ('detail', models.CharField(default='', max_length=100)),
                ('created_by', models.IntegerField(default=1)),
                ('deleted', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'advice',
            },
        ),
        migrations.CreateModel(
            name='AdviceGroupModel',
            fields=[
                ('advice_group_id', models.AutoField(primary_key=True, serialize=False)),
                ('advice_group', models.CharField(default='', max_length=50)),
                ('created_by', models.IntegerField(default=1)),
                ('deleted', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('advice', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='advice.advicemodel')),
            ],
            options={
                'db_table': 'advice_group',
            },
        ),
    ]