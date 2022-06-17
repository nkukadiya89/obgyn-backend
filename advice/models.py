from operator import mod
from django.db import models
from django.utils.timezone import now


# Create your models here.
class AdviceModel(models.Model):
    advice_for_choice = (
        ("OPD", "OPD"),
        ("SONOGRAPHY", "SONOGRAPHY"),
        ("GENERAL", "GENERAL"),
        ("POST-CS", "POST-CS"),
        ("PRE-CS", "PRE-CS"),
    )
    advice_id = models.AutoField(primary_key=True)
    advice = models.TextField(null=True)
    advice_for = models.CharField(
        max_length=15, choices=advice_for_choice, null=False, default="OPD"
    )
    detail = models.CharField(max_length=100, default="", blank=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "advice"
        app_label = "adivce"


class AdviceGroupModel(models.Model):
    advice_group_id = models.AutoField(primary_key=True)
    advice_group = models.CharField(max_length=50, default="")
    advice = models.ManyToManyField(AdviceModel, blank=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = "advice_group"


class AdviceGroupAdviceModel(models.Model):
    id = models.AutoField(primary_key=True)
    advicegroupmodel_id = models.IntegerField()
    advicemodel_id = models.IntegerField()

    class Meta:
        db_table = "advice_group_advice"
        managed = False
