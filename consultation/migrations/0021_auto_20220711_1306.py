# Generated by Django 3.2.9 on 2022-07-11 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0020_alter_consultationmodel_breast'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultationmodel',
            name='mh_every',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='consultationmodel',
            name='mh_for',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='consultationmodel',
            name='mh_severity',
            field=models.CharField(default='', max_length=25, null=True),
        ),
    ]
