from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientIndoorModel, IndoorAdviceModel


class PatientIndoorSerializers(serializers.ModelSerializer):
    def validate(self, data):
        if "patient_opd_id" not in data:
            raise serializers.ValidationError("OPD is required.")

        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        return data

    patient_indoor_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientIndoorModel
        exclude = ('created_at', 'patient')


class IndoorAdviceSerializers(serializers.ModelSerializer):

    indoor_advice_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = IndoorAdviceModel
        exclude = ('created_at',)
