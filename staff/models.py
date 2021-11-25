from user.models import User
from django.db import models
from django.utils.timezone import now


# Create your models here.

class StaffModel(models.Model):
    staff_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aadhar_card = models.CharField(max_length=15)
    designation = models.CharField(max_length=25)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.staff_id})"

    class Meta:
        db_table = "staff"
