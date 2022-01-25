from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientOpdModel


class PatientOpdSerializers(serializers.ModelSerializer):
    def validate(self, data):
        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id

        patient_opd = PatientOpdModel.objects.filter(opd_date=data["opd_date"], patient_id=data["patient_id"])
        if len(patient_opd) > 0:
            raise serializers.ValidationError("Patient visited today.")

        return data

    patient_opd_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientOpdModel
        exclude = ('created_at', 'patient')
