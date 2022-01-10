from django.db import models
from django.utils.timezone import now


# Create your models here.
class AdviseModel(models.Model):
    advise_for_choice = (
        ('OPD', 'OPD'),
        ('SONOGRAPHY', 'SONOGRAPHY'),
        ('GENERAL', 'GENERAL')
    )
    advise_id = models.AutoField(primary_key=True)
    advise = models.TextField(null=True)
    advise_for = models.CharField(max_length=15, choices=advise_for_choice, null=False, default="OPD")

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = 'advise'
