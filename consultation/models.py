from django.db import models
from django.utils.timezone import now

from advice.models import AdviceModel
from diagnosis.models import DiagnosisModel
from manage_fields.models import ManageFieldsModel
from patient.models import PatientModel
from patient_opd.models import PatientOpdModel


# Create your models here.

class ConsultationModel(models.Model):
    parity_choice = (
        ('PRIMI', 'PRIMI'),
        ('MULTI', 'MUTLI')
    )

    prev_del_choice = (
        ('NORMAL', 'NORMAL'),
        ('CESAREAN', 'CESAREAN')
    )

    consultation_id = models.AutoField(primary_key=True)
    patient_opd = models.ForeignKey(PatientOpdModel, on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING, null=True)
    parity = models.CharField(max_length=15, choices=parity_choice, default='PRIMI')
    prev_del_type = models.CharField(max_length=15, choices=prev_del_choice, default="NORMAL")
    present_history = models.CharField(max_length=250, default="")
    past_history = models.CharField(max_length=250, default="")
    family_history = models.CharField(max_length=250, default="")
    opd_date = models.DateField(default=now)
    regd_no = models.CharField(max_length=100, default="")
    lmp_date = models.DateField(default=now)
    edd_date = models.DateField(default=now)

    ftnd_male_live = models.IntegerField(default=0)
    ftnd_male_dead = models.IntegerField(default=0)
    ftnd_female_live = models.IntegerField(default=0)
    ftnd_female_dead = models.IntegerField(default=0)

    ftlscs_male_live = models.IntegerField(default=0)
    ftlscs_male_dead = models.IntegerField(default=0)
    ftlscs_female_live = models.IntegerField(default=0)
    ftlscs_female_dead = models.IntegerField(default=0)

    ho = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="ho")
    co = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="co")
    possible_lmp = models.DateField(default=now)
    possible_edd = models.DateField(default=now)
    temprature = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="temprature")
    puls = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="puls")
    bp = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="bp")
    resperistion = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True,
                                     related_name="resperistion")
    spo2 = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="spo2")
    pallor = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="pallor")
    lcterus = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="lcterus")
    oedema = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="oedema")
    rs = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="rs")
    cvs = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="cvs")
    breast = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="breast")
    pa_gyn = models.BooleanField(default=False)
    pa_obs = models.BooleanField(default=False)
    pv = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="pv")
    tt = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="tt")
    diagnosis = models.ForeignKey(DiagnosisModel, on_delete=models.DO_NOTHING, null=True)
    advice = models.ForeignKey(AdviceModel, on_delete=models.DO_NOTHING, null=True)
    fu = models.IntegerField(null=True)
    fu_date = models.DateField(default=now)
    remark = models.TextField(null=True)

    # ================= investigation===================
    hb = models.CharField(max_length=50, default="")
    blood_group = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True,
                                    related_name="blood_group")
    urine_sugar = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True,
                                    related_name="urine_sugar")
    urine_protein = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True,
                                      related_name="urine_protein")
    hiv = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="hiv")
    hbsag = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="hbsag")
    tsh = models.CharField(max_length=50, default="")
    vdrl = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="vdrl")

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.consultation_id})"

    class Meta:
        db_table = "consultation"
