# Generated by Django 3.2.9 on 2023-04-29 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obgyn_config', '0016_obgynconfigmodel_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='obgynconfigmodel',
            name='usg_or_pa',
            field=models.CharField(default='', max_length=15, null=True),
        ),
    ]