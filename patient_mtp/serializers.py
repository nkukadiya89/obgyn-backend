from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientMtpModel
from manage_fields.serializers import ManageFieldsSerializers


class PatientMtpSerializers(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(PatientMtpSerializers, self).to_representation(instance)

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
    admission_date = serializers.DateField(format="%d-%m-%Y")
    procedure_date = serializers.DateField(format="%d-%m-%Y")
    termination_date = serializers.DateField(format="%d-%m-%Y")
    discharge_date = serializers.DateField(format="%d-%m-%Y")
    

    class Meta:
        model = PatientMtpModel
        exclude = ('created_at', 'patient')
