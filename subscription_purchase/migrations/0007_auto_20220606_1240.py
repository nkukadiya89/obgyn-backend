# Generated by Django 3.2.9 on 2022-06-06 07:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_purchase', '0006_alter_subscription_purchasemodel_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription_purchasemodel',
            name='over_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='subscription_purchasemodel',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]