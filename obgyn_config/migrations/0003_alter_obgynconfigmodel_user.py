# Generated by Django 3.2.9 on 2022-04-25 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('obgyn_config', '0002_rename_obgynconfig_obgynconfigmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='obgynconfigmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
