from django.db import models
from django.utils.timezone import now

from patient.models import PatientModel
from patient_opd.models import PatientOpdModel
from surgical_item.models import SurgicalItemModel

# Create your models here.
class PatientVoucherModel(models.Model):
    patient_voucher_id = models.AutoField(primary_key=True)
    patient_opd = models.ForeignKey(PatientOpdModel, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    voucher_no = models.CharField(max_length=25,default="")
    bill_date = models.DateField(null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_voucher_id})"

    class Meta:
        db_table = "patient_voucher"



class VoucherItemModel(models.Model):
    voucher_item_id = models.AutoField(primary_key=True)
    patient_voucher = models.ForeignKey(PatientVoucherModel, on_delete=models.CASCADE)

    surgical_item = models.ForeignKey(SurgicalItemModel, on_delete=models.DO_NOTHING)
    unit = models.IntegerField(default=0)
    rate = models.FloatField(default=0)
    total_amount = models.FloatField(default=0.0)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.voucher_item_id})"

    class Meta:
        db_table = "voucher_item"
