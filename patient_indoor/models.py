from django.db import models
from django.db.models.query import Q
from django.db.models.signals import post_save
from django.utils.timezone import now

from financial_year.models import FinancialYearModel
from advice.models import AdviceModel
from diagnosis.models import DiagnosisModel
from patient.models import PatientModel
from patient_opd.models import PatientOpdModel
from manage_fields.models import ManageFieldsModel


# Create your models here.
class PatientIndoorModel(models.Model):
    patient_indoor_id = models.AutoField(primary_key=True)
    patient_opd = models.ForeignKey(PatientOpdModel, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    indoor_case_number = models.CharField(max_length=100, default="", null=True)
    indoor_date = models.DateField(null=True)
    indoor_time = models.CharField(max_length=15, null=True)
    complain = models.CharField(max_length=500, null=True)
    temprature = models.CharField(max_length=25, default="", null=True)
    pulse = models.FloatField(default=0.0, null=True)
    bp = models.CharField(max_length=25, default="", null=True)
    spo2 = models.CharField(max_length=15, default="", null=True)
    pallor = models.CharField(max_length=25, default="", null=True)
    lcterus = models.CharField(max_length=25, default="", null=True)
    oedema = models.CharField(max_length=25, default="", null=True)
    rs = models.CharField(max_length=25, default="", null=True)
    cvs = models.CharField(max_length=25, default="", null=True)
    pa_gyn = models.CharField(max_length=25, default="", null=True)
    pa_obs = models.CharField(max_length=25, default="", null=True)
    ut_weeks = models.IntegerField(default=0, null=True)
    eb_pp = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="eb_pp_indr")
    fhs = models.CharField(max_length=25, default="", null=True)
    ut = models.CharField(max_length=25, default="", null=True)
    ps = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="ps_indr")
    pv = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="pv_indr")
    ut_contra = models.CharField(max_length=25, default="", null=True)
    adm_date = models.DateField(null=True)
    adm_time = models.CharField(max_length=15, default="", null=True)
    oper_date = models.DateField(null=True)
    oper_time = models.CharField(max_length=15, default="", null=True)
    disch_date = models.DateField(null=True)
    disch_time = models.CharField(max_length=15, default="", null=True)
    operation = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="operation_indr")
    diagnosis = models.ForeignKey(DiagnosisModel, on_delete=models.DO_NOTHING, null=True)
    provisional_diagnosis = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="provisional_diagnosis") 
    daistolic_bp = models.CharField(max_length=15, default="", null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_indoor_id})"

    class Meta:
        db_table = "patient_indoor"


class IndoorAdviceModel(models.Model):
    indoor_advice_id = models.AutoField(primary_key=True)
    patient_indoor = models.ForeignKey(PatientIndoorModel, on_delete=models.CASCADE)

    advice = models.ForeignKey(AdviceModel, on_delete=models.DO_NOTHING)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.indoor_advice_id})"

    class Meta:
        db_table = "indoor_advice"


def indoor_post_save(sender, instance, *args, **kwargs):
    if kwargs["created"]:
        fy = FinancialYearModel.objects.filter(start_date__lte=now(), end_date__gte=now()).values_list(
            'financial_year').first()

        indoor = PatientIndoorModel.objects.filter(~Q(pk=instance.patient_indoor_id)).filter(deleted=0,
                                                                                                indoor_case_number__icontains=
                                                                                                fy[0]).last()

        if indoor:
            case_no = indoor.indoor_case_number

            if not case_no or len(case_no) == 0:
                case_no = "I/00001/" + fy[0]
            else:
                serial_no = case_no.split("/")[1]
                serial_no = int(serial_no) + 1
                case_no = "ICN/" + '{:05}'.format(serial_no) + "/" + fy[0]
        else:
            case_no = "ICN/00001/" + fy[0]

        instance.indoor_case_number = case_no
        instance.save()


post_save.connect(indoor_post_save, sender=PatientIndoorModel)