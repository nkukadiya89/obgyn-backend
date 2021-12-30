# Generated by Django 3.2.9 on 2021-12-28 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0004_auto_20211228_1610'),
        ('manage_fields', '0002_auto_20211226_1841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='managefieldsmodel',
            old_name='createdAt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='managefieldsmodel',
            old_name='createdBy',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='managefieldsmodel',
            old_name='fieldName',
            new_name='field_name',
        ),
        migrations.RenameField(
            model_name='managefieldsmodel',
            old_name='fieldValue',
            new_name='field_value',
        ),
        migrations.RenameField(
            model_name='managefieldsmodel',
            old_name='mfId',
            new_name='mf_id',
        ),
        migrations.AlterField(
            model_name='managefieldsmodel',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='language.languagemodel'),
        ),
    ]