# Generated by Django 3.2.9 on 2022-04-25 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ObgynConfig',
            fields=[
                ('obgyn_config_id', models.AutoField(primary_key=True, serialize=False)),
                ('rs_per_visit', models.FloatField(default=0, null=True)),
                ('rs_per_usg', models.FloatField(default=0, null=True)),
                ('rs_per_room', models.FloatField(default=0, null=True)),
                ('operative_charge', models.FloatField(default=0, null=True)),
                ('rs_per_day_nursing', models.FloatField(default=0, null=True)),
                ('monthly_usg', models.IntegerField(default=0, null=True)),
                ('yearly_usg', models.IntegerField(default=0, null=True)),
                ('created_by', models.IntegerField(default=1)),
                ('deleted', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'obgyn_config',
            },
        ),
    ]
