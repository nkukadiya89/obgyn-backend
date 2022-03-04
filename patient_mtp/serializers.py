from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientMtpModel
from manage_fields.serializers import ManageFieldsSerializers


class PatientMtpSerializers(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(PatientMtpSerializers, self).to_representation(instance)

        for fld_nm in ["reason_for_mtp"]:
            fld_name = fld_nm + "_name"
            search_instance = "instance" + "." + fld_nm
            if fld_nm in ret:
                ret[fld_name] = ManageFieldsSerializers(eval(search_instance)).data["field_value"]


        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]
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

    class Meta:
        model = PatientMtpModel
        exclude = ('created_at', 'patient')
