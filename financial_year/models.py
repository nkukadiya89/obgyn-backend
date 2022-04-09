from django.db import models
from django.utils.timezone import now


# Create your models here.
class FinancialYearModel(models.Model):
    fid = models.AutoField(primary_key=True)
    financial_year = models.CharField(max_length=15, default="")
    start_date = models.DateField(default=now)
    end_date = models.DateField(default=now)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.fid} )"

    class Meta:
        db_table = "financial_year"
