# Generated by Django 3.2.9 on 2021-12-26 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surgical_item', '0003_auto_20211226_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='surgicalitemgroupmodel',
            name='surgical_item',
            field=models.ManyToManyField(to='surgical_item.SurgicalItemModel'),
        ),
    ]
