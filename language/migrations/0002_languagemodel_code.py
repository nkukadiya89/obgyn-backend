# Generated by Django 3.2.9 on 2021-12-23 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='languagemodel',
            name='code',
            field=models.CharField(default='', max_length=5),
        ),
    ]
