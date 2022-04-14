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
    consultation_id = models.AutoField(primary_key=True)
    patient_opd = models.OneToOneField(PatientOpdModel, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING, null=True)
    parity = models.CharField(max_length=25, default="")
    prev_del_type = models.CharField(max_length=25, default="")
    present_history = models.CharField(max_length=250, default="")
    past_history = models.CharField(max_length=250, default="")
    family_history = models.CharField(max_length=250, default="")
    opd_date = models.DateField(default=now)
    regd_no = models.CharField(max_length=100, default="")
    lmp_date = models.DateField(default=now)
    edd_date = models.DateField(default=now)

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

    ho = models.CharField(max_length=25, default="")
    co = models.CharField(max_length=25, default="")
    possible_lmp = models.DateField(default=now, null=True)
    possible_edd = models.DateField(default=now, null=True)
    temprature = models.CharField(max_length=25, default="")
    puls = models.IntegerField(default=0, null=True)
    bp = models.CharField(max_length=10, null=True)
    resperistion = models.IntegerField(default=0, null=True)
    spo2 = models.CharField(max_length=6, null=True)
    pallor = models.CharField(max_length=100, default="")
    lcterus = models.CharField(max_length=25, default="")
    oedema = models.CharField(max_length=25, default="")
    rs = models.CharField(max_length=25, default="")
    cvs = models.CharField(max_length=25, default="")
    breast = models.CharField(max_length=25, default="")
    pa_gyn = models.BooleanField(default=False, null=True)
    pa_value = models.CharField(max_length=25,default="")
    pa_obs = models.BooleanField(default=False, null=True)
    ut_weeks = models.IntegerField(default=0)
    ut_days = models.IntegerField(default=0)
    eb_pp = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="eb_pp")
    fhs = models.CharField(max_length=25, default="")
    ut = models.CharField(max_length=25, default="")
    ps = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="ps")
    pv = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="pv")
    diagnosis = models.ForeignKey(DiagnosisModel, on_delete=models.DO_NOTHING, null=True)
    advice = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="advice")
    fu = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="fu")
    fu_date = models.DateField(default=now, null=True)
    remark = models.TextField(null=True)

    # ================= investigation===================
    hb = models.CharField(max_length=50, default="", null=True)
    blood_group = models.CharField(max_length=25, default="", null=True)
    urine_sugar = models.CharField(max_length=25, default="", null=True)
    urine_protein = models.CharField(max_length=25, default="", null=True)
    hiv = models.CharField(max_length=25, default="", null=True)
    hbsag = models.CharField(max_length=25, default="", null=True)
    tsh = models.CharField(max_length=25, default="", null=True)
    vdrl = models.CharField(max_length=25, default="", null=True)
    other = models.TextField(null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.consultation_id})"

    class Meta:
        db_table = "consultation"

