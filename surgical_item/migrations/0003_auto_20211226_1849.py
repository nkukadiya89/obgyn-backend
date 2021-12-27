# Generated by Django 3.2.9 on 2021-12-26 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surgical_item', '0002_surgicalitemgroupmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surgicalitemgroupmodel',
            old_name='created_at',
            new_name='createdAt',
        ),
        migrations.RenameField(
            model_name='surgicalitemgroupmodel',
            old_name='created_by',
            new_name='createdBy',
        ),
        migrations.RenameField(
            model_name='surgicalitemgroupmodel',
            old_name='drug_name',
            new_name='drugName',
        ),
        migrations.RenameField(
            model_name='surgicalitemgroupmodel',
            old_name='si_group_id',
            new_name='siGroupId',
        ),
        migrations.RenameField(
            model_name='surgicalitemmodel',
            old_name='batch_number',
            new_name='batchNumber',
        ),
        migrations.RenameField(
            model_name='surgicalitemmodel',
            old_name='created_at',
            new_name='createdAt',
        ),
        migrations.RenameField(
            model_name='surgicalitemmodel',
            old_name='created_by',
            new_name='createdBy',
        ),
        migrations.RenameField(
            model_name='surgicalitemmodel',
            old_name='drug_name',
            new_name='drugName',
        ),
        migrations.RenameField(
            model_name='surgicalitemmodel',
            old_name='exp_date',
            new_name='expDate',
        ),
        migrations.RenameField(
            model_name='surgicalitemmodel',
            old_name='mfg_date',
            new_name='mfgDate',
        ),
        migrations.RenameField(
            model_name='surgicalitemmodel',
            old_name='surgical_item_id',
            new_name='surgicalItemId',
        ),
        migrations.RemoveField(
            model_name='surgicalitemgroupmodel',
            name='surgical_item',
        ),
    ]
