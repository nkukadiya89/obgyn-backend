# Generated by Django 3.2.9 on 2022-05-18 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0015_auto_20220506_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultationmodel',
            name='resperistion',
            field=models.CharField(max_length=5, null=True),
        ),
    ]