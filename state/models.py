from django.db import models
from django.utils.timezone import now

# Create your models here.
class StateModel(models.Model):
    stateId = models.AutoField(primary_key=True)
    stateName = models.CharField(max_length=50)

    createdBy = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    createdAt = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.stateId},{self.stateName})"

    class Meta:
        db_table = "state"
