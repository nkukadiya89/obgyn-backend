# Generated by Django 3.2.9 on 2022-03-07 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0007_rename_no_of_femaile_consultationmodel_no_of_female'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultationmodel',
            name='pa_value',
            field=models.CharField(default='', max_length=25),
        ),
    ]