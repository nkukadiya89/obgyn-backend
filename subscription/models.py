from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now

# Create your models here.
class SubscriptionModel(models.Model):
    subscription_id = models.AutoField(primary_key=True)
    subscription_name = models.CharField(max_length=50)

    actual_price = models.IntegerField()
    discount = models.IntegerField()
    sell_price = models.IntegerField()
    duration = models.IntegerField()
    description = models.CharField(max_length=100)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)


    def __str__(self):
        return f"({self.subscription_id},{self.subscription_name})"

    class Meta:
        db_table = "subscription"

