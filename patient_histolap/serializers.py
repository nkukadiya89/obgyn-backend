from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientHistolapModel


class PatientHistolapSerializers(serializers.ModelSerializer):
    def validate(self, data):
        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        return data

    patient_histolap_id = serializers.IntegerField(read_only=True)
    admission_date = serializers.DateField(format="%d-%m-%Y",)
    discharge_date = serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = PatientHistolapModel
        exclude = ('created_at', 'patient')
