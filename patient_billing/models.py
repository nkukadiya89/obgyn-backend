from re import T
from django.db import models
from django.db.models.query import Q
from django.db.models.signals import post_save
from django.utils.timezone import now

from diagnosis.models import DiagnosisModel
from financial_year.models import FinancialYearModel
from patient.models import PatientModel
from patient_opd.models import PatientOpdModel
from manage_fields.models import ManageFieldsModel


# Create your models here.
class PatientBillingModel(models.Model):
    patient_billing_id = models.AutoField(primary_key=True)
    patient_opd = models.ForeignKey(PatientOpdModel, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    invoice_no = models.CharField(max_length=25, null=True)
    admission_date = models.DateField(null=True)
    admission_time = models.CharField(max_length=10, null=True)
    ot_date = models.DateField(null=True)
    ot_time = models.CharField(max_length=10, null=True)
    discharge_date = models.DateField(null=True)
    discharge_time = models.CharField(max_length=10, null=True)
    diagnosis = models.ForeignKey(DiagnosisModel, on_delete=models.DO_NOTHING)
    procedure_name = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, related_name="billing_procedure_name", null=True)
    no_of_visit = models.IntegerField(default=0)
    rs_per_visit = models.FloatField(default=0.0)
    consulting_fees = models.FloatField(default=0.0)
    no_of_usg = models.IntegerField(default=0)
    rs_per_usg = models.FloatField(default=0.0)
    usg_rs = models.FloatField(default=0.0)
    room_no_of_day = models.CharField(max_length=25, null=True)
    rs_per_room = models.FloatField(default=0.0)
    room_type = models.CharField(max_length=25, default="", null=True)
    room_rs = models.FloatField(default=0.0)
    procedure_charge = models.FloatField(default=0.0)
    medicine_rs = models.FloatField(default=0.0)
    nursing_no_of_days = models.IntegerField(default=0)
    rs_per_day = models.FloatField(default=0.0)
    nursing_rs = models.FloatField(default=0.0)
    other_charge = models.CharField(max_length=250, null=True)
    other_rs = models.FloatField(default=0.0)
    total_rs = models.FloatField(default=0.0)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_billing_id})"

    class Meta:
        db_table = "patient_billing"


def billing_post_save(sender, instance, *args, **kwargs):
    if kwargs["created"]:
        fy = FinancialYearModel.objects.filter(start_date__lte=now(), end_date__gte=now()).values_list(
            'financial_year').first()

        billing = PatientBillingModel.objects.filter(~Q(pk=instance.patient_billing_id)).filter(deleted=0,
                                                                                                invoice_no__icontains=
                                                                                                fy[0]).last()

        if billing:
            inv_no = billing.invoice_no

            if not inv_no or len(inv_no) == 0:
                inv_no = "I/00001/" + fy[0]
            else:
                serial_no = inv_no.split("/")[1]
                serial_no = int(serial_no) + 1
                inv_no = "I/" + '{:05}'.format(serial_no) + "/" + fy[0]
        else:
            inv_no = "I/00001/" + fy[0]

        instance.invoice_no = inv_no
        instance.save()


post_save.connect(billing_post_save, sender=PatientBillingModel)
