from django.db import models
from django.utils.timezone import now

from diagnosis.models import DiagnosisModel
from patient.models import PatientModel
from patient_opd.models import PatientOpdModel
from manage_fields.models import ManageFieldsModel


# Create your models here.
class PatientUSGFormModel(models.Model):
    patient_usgform_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(PatientModel, on_delete=models.DO_NOTHING)
    patient_opd = models.OneToOneField(PatientOpdModel, on_delete=models.DO_NOTHING)
    regd_no = models.CharField(max_length=100, default="")

    ut_weeks = models.IntegerField(default=0)
    lmp_date = models.DateField(null=True)
    diagnosis = models.ForeignKey(DiagnosisModel, on_delete=models.DO_NOTHING)
    indication = models.ManyToManyField(ManageFieldsModel, blank=True)
    usg_image_no = models.CharField(max_length=25, null=True)
    result_of_sonography = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="result_of_sonography")
    serial_no_month = models.IntegerField(default=0, null=True)
    serial_no_year = models.IntegerField(default=0, null=True)
    ref_by_dr = models.CharField(max_length=150, default="", null=True)
    village = models.CharField(max_length=100, default="", null=True)
    taluka = models.CharField(max_length=100, default="", null=True)
    doctor_center_taluka_district = models.CharField(max_length=250,null=True)
    any_other = models.CharField(max_length=150,null=True)
    doctor_address = models.TextField(null=True)
    name_of_doctor = models.CharField(max_length=150,null=True)
    consent_obtained_date = models.DateField(default=now, null=True)
    procedure_date = models.DateField(default=now, null=True)
    result_of_diagnostic_conveyed_to = models.CharField(max_length=250,null=True)
    sonography_date = models.DateField(default=now, null=True)
    any_indication_mtp = models.ForeignKey(ManageFieldsModel, on_delete=models.DO_NOTHING, null=True, related_name="any_indication_mtp")
    mtp_done = models.CharField(max_length=100, null=True)
    remark = models.TextField(null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.patient_usgform_id})"

    class Meta:
        db_table = "patient_usgform"


class USGFormChildModel(models.Model):
    gender_choice = (
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE")
    )

    usgform_child_id = models.AutoField(primary_key=True)
    patient_usgform = models.ForeignKey(PatientUSGFormModel, on_delete=models.DO_NOTHING)
    child_gender = models.CharField(max_length=10, choices=gender_choice, default="MALE")
    child_year = models.IntegerField(null=True)
    child_month = models.IntegerField(null=True)

    created_by = models.IntegerField(default=1, unique=False)
    deleted = models.IntegerField(default=0, unique=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"({self.usgform_child_id})"

    class Meta:
        db_table = "usgform_child"


