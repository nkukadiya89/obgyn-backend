# Generated by Django 3.2.9 on 2022-06-17 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_authgroupmodel_authgrouppermissionsmodel_authpermissionmodel_contenttypemodel_usergroupsmodel'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='contenttypemodel',
            table='django_content_type',
        ),
    ]
