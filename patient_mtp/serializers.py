from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientMtpModel
from consultation.models import ConsultationModel
from manage_fields.serializers import ManageFieldsSerializers


class PatientMtpSerializers(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(PatientMtpSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]

        for fld_nm in ["religion"]:
            fld_name = fld_nm + "_name"
            search_instance = "instance" + "." + fld_nm
            if fld_nm in ret:
                ret[fld_name] = ManageFieldsSerializers(eval(search_instance)).data[
                    "field_value"
                ]
        consultation = ConsultationModel.objects.filter(
            patient_opd=instance.patient_opd, deleted=0
        ).order_by('created_at').first()

        if consultation:
            ret["ut_weeks_c"] = consultation.ut_weeks
            if consultation.ut_weeks:
                ret["second_rmp_c"] = "-" if consultation.ut_weeks <= 12 else None
            else:
                ret["second_rmp_c"] = None


        return ret

    def validate(self, data):
        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        return data

    patient_mtp_id = serializers.IntegerField(read_only=True)
    admission_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    procedure_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    termination_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    discharge_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    

    class Meta:
        model = PatientMtpModel
        exclude = ('created_at', 'patient')
