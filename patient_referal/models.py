from django.db import models
from django.utils.timezone import now

from manage_fields.models import ManageFieldsModel
from patient.models import PatientModel
from patient_opd.models import PatientOpdModel


# Create your models here.
class PatientReferalModel(models.Model):
    patient_referal_id = models.AutoField(primary_key=True)
    patient_opd = models.OneToOneField(PatientOpdModel, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")
    indication = models.ManyToManyField(ManageFieldsModel,blank=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_referal_id},{self.indication})"

    class Meta:
        db_table = "patient_referal"
