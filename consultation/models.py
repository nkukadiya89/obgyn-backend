from re import T
from django.db import models
from django.utils.timezone import now

from advice.models import AdviceModel
from diagnosis.models import DiagnosisModel
from manage_fields.models import ManageFieldsModel
from patient.models import PatientModel
from patient_opd.models import PatientOpdModel


# Create your models here.

class ConsultationModel(models.Model):

    
    patient_type_choice = (
        ("OB", "OB"),
        ("GYN", "GYN")
    )
    patient_detail_choice = (
        ("FULL", "FULL"),
        ("PARTIAL", "PARTIAL")
    )

    consultation_id = models.AutoField(primary_key=True)
    patient_opd = models.OneToOneField(PatientOpdModel, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING, null=True)
    
    patient_type = models.CharField(max_length=5, choices=patient_type_choice, default="OB")
    patient_detail = models.CharField(max_length=8, choices=patient_detail_choice, default="PARTIAL")
    parity = models.CharField(max_length=25, default="", null=True)
    prev_del_type = models.CharField(max_length=25, default="", null=True)
    present_history = models.CharField(max_length=250, default="", null=True)
    past_history = models.CharField(max_length=250, default="", null=True)
    family_history = models.CharField(max_length=250, default="", null=True)
    opd_date = models.DateField(default=now, null=True)
    regd_no = models.CharField(max_length=100, default="", null=True)
    lmp_date = models.DateField(default=now, null=True)
    edd_date = models.DateField(default=now, null=True)

    no_of_male = models.IntegerField(default=0, null=True)
    no_of_female = models.IntegerField(default=0, null=True)

    ftnd_male_live = models.IntegerField(default=0, null=True)
    ftnd_male_dead = models.IntegerField(default=0, null=True)
    ftnd_female_live = models.IntegerField(default=0, null=True)
    ftnd_female_dead = models.IntegerField(default=0, null=True)

    ftlscs_male_live = models.IntegerField(default=0, null=True)
    ftlscs_male_dead = models.IntegerField(default=0, null=True)
    ftlscs_female_live = models.IntegerField(default=0, null=True)
    ftlscs_female_dead = models.IntegerField(default=0, null=True)

    ho = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="ho")
    co = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="co")
    possible_lmp = models.DateField(default=now, null=True)
    possible_edd = models.DateField(default=now, null=True)
    temprature = models.CharField(max_length=25, default="", null=True)
    puls = models.IntegerField(default=0, null=True)
    bp = models.CharField(max_length=10, null=True)
    resperistion = models.CharField(max_length=10, null=True)
    spo2 = models.IntegerField(default=0, null=True)
    pallor = models.CharField(max_length=100, default="", null=True)
    lcterus = models.CharField(max_length=25, default="", null=True)
    oedema = models.CharField(max_length=25, default="", null=True)
    rs = models.CharField(max_length=25, default="", null=True)
    cvs = models.CharField(max_length=25, default="", null=True)
    breast = models.CharField(max_length=25, default="", null=True)
    pa_gyn = models.BooleanField(default=False, null=True)
    pa_value = models.CharField(max_length=25,default="", null=True)
    pa_obs = models.BooleanField(default=False, null=True)
    ut_weeks = models.IntegerField(default=0, null=True)
    ut_days = models.IntegerField(default=0, null=True)
    eb_pp = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="eb_pp")
    fhs = models.CharField(max_length=25, default="", null=True)
    ut = models.CharField(max_length=25, default="", null=True)
    ps = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="ps")
    pv = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="pv")
    diagnosis = models.ForeignKey(DiagnosisModel, on_delete=models.DO_NOTHING, null=True)
    # advice = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="advice")
    advice = models.CharField(max_length=750, null=True)
    fu = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="fu")
    fu_date = models.DateField(default=now, null=True)
    remark = models.TextField(null=True)

    # ================= investigation===================
    hb = models.IntegerField( default=0, null=True)
    blood_group = models.CharField(max_length=25, default="", null=True)
    urine_sugar = models.CharField(max_length=25, default="", null=True)
    urine_protein = models.CharField(max_length=25, default="", null=True)
    hiv = models.CharField(max_length=25, default="", null=True)
    hbsag = models.CharField(max_length=25, default="", null=True)
    tsh = models.FloatField(default=0, null=True)
    vdrl = models.CharField(max_length=25, default="", null=True)
    other = models.TextField(null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.consultation_id})"

    class Meta:
        db_table = "consultation"

