# Generated by Django 3.2.9 on 2022-05-24 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_fields', '0005_alter_managefieldsmodel_field_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldmastermodel',
            name='slug',
            field=models.SlugField(max_length=150, null=True),
        ),
    ]
