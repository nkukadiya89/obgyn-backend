# Generated by Django 3.2.9 on 2022-06-06 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_purchase', '0005_rename_subscription_purchase_id_subscription_purchasemodel_subscription_purchase_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription_purchasemodel',
            name='description',
            field=models.CharField(default='', max_length=250),
        ),
    ]
