# Generated by Django 3.2.9 on 2022-04-01 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advice', '0004_alter_advicemodel_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advicegroupmodel',
            name='advice',
            field=models.ManyToManyField(blank=True, to='advice.AdviceModel'),
        ),
    ]