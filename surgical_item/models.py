from django.db import models
from django.utils.timezone import now

from user.models import User


# Create your models here.
class SurgicalItemModel(models.Model):
    surgical_item_id = models.AutoField(primary_key=True)
    drug_name = models.CharField(max_length=150, default="")
    mrp = models.FloatField(default=0)
    batch_number = models.CharField(max_length=50, default="")
    mfg_date = models.CharField(max_length=25, default="")
    exp_date = models.CharField(max_length=25, default="")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.surgical_item_id},{self.drug_name})"

    class Meta:
        db_table = "surgical_item"


class SurgicalItemGroupModel(models.Model):
    si_group_id = models.AutoField(primary_key=True)
    drug_group_name = models.CharField(max_length=150, default="")
    surgical_item = models.ManyToManyField(SurgicalItemModel, blank=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.si_group_id},{self.drug_name})"

    class Meta:
        db_table = "surgical_item_group"


class SurgicalItemGroupSurgicalItem(models.Model):
    id = models.AutoField(primary_key=True)
    surgicalitemgroupmodel_id = models.IntegerField()
    surgicalitemmodel_id = models.IntegerField()

    class Meta:
        db_table = "surgical_item_group_surgical_item"
        managed = False
