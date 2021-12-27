# Generated by Django 3.2.9 on 2021-12-26 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('language', '0003_auto_20211226_1839'),
        ('state', '0002_auto_20211226_1845'),
        ('city', '0002_auto_20211226_1635'),
        ('user', '0003_alter_user_default_language'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='aadhar_card',
            new_name='aadharCard',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='created_at',
            new_name='createdAt',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='created_by',
            new_name='createdBy',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='fax_number',
            new_name='faxNumber',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='hospital_name',
            new_name='hospitalName',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='middle_name',
            new_name='middleName',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='registration_no',
            new_name='registrationNo',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_type',
            new_name='userType',
        ),
        migrations.RemoveField(
            model_name='user',
            name='default_language',
        ),
        migrations.AddField(
            model_name='user',
            name='defaultLanguage',
            field=models.ForeignKey(db_column='defaultLanguageId', default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='language.languagemodel'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_code',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.ForeignKey(db_column='cityId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='city.citymodel'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(db_column='firstName', default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='hospital',
            field=models.ForeignKey(db_column='hospitalId', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(db_column='lastName', default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='state',
            field=models.ForeignKey(db_column='stateId', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='state.statemodel'),
        ),
    ]
