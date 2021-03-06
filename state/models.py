from django.db import models
from django.utils.timezone import now

# Create your models here.
class StateModel(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=50)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.state_id},{self.state_name})"

    class Meta:
        db_table = "state"
