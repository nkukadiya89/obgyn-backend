# Generated by Django 3.2.9 on 2022-06-17 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_user_landmark'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroupModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissionsModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermissionModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContentTypeModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserGroupsModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'user_groups',
                'managed': False,
            },
        ),
    ]
