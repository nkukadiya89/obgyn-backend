from operator import mod
from django.db import models
from django.db import models
from django.utils.timezone import now
from datetime import datetime
from user.models import User
from subscription.models import SubscriptionModel


class Subscription_purchaseModel(models.Model):

    subscription_purchase_id = models.AutoField(primary_key=True)

    hospital = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    subscription = models.ForeignKey(SubscriptionModel, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(default=0)
    duration = models.IntegerField(default=0)

    start_date = models.DateField()
    over_date = models.DateField()

    description = models.CharField(max_length=250, default="")

    inactive = models.BooleanField(default=False)
    discount = models.IntegerField(default=0)
    payment_id = models.IntegerField(default=0)
    order_id = models.IntegerField(default=0)
    invoice_no = models.IntegerField(default=0)
    inv_year = models.CharField(max_length=15, default="")

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateField(default=now)


    def __str__(self):
        return f"({self.subscription_purchase_id})"

    class Meta:
        db_table = "subscription_purchase"