# Generated by Django 3.2.9 on 2021-12-28 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('state', '0003_auto_20211228_1343'),
        ('user', '0009_alter_user_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to='state.statemodel'),
        ),
    ]
