# Generated by Django 3.2.9 on 2022-01-18 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advice', '0002_auto_20220118_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advicemodel',
            name='advice_group',
        ),
        migrations.AddField(
            model_name='advicegroupmodel',
            name='advice',
            field=models.ManyToManyField(to='advice.AdviceModel'),
        ),
    ]
