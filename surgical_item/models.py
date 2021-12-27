from django.db import models
from django.utils.timezone import now

from user.models import User


# Create your models here.
class SurgicalItemModel(models.Model):
    surgicalItemId = models.AutoField(primary_key=True)
    drugName = models.CharField(max_length=150, default="")
    mrp = models.FloatField(default=0)
    batchNumber = models.CharField(max_length=50, default="")
    mfgDate = models.DateField(default=now)
    expDate = models.DateField(default=now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    createdBy = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    createdAt = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.surgicalItemId},{self.drugName})"

    class Meta:
        db_table = "surgical_item"


class SurgicalItemGroupModel(models.Model):
    siGroupId = models.AutoField(primary_key=True)
    drugName = models.CharField(max_length=150, default="")
    surgical_item = models.ManyToManyField(SurgicalItemModel)

    createdBy = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    createdAt = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.siGroupId},{self.drugName})"

    class Meta:
        db_table = "surgical_item_group"
