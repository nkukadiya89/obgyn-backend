from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientMtpModel


class PatientMtpSerializers(serializers.ModelSerializer):
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
