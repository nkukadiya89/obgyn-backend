from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientOvulationProfileModel


class PatientOvulationProfileSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientOvulationProfileSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]
        return ret

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

    patient_ovulation_profile_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientOvulationProfileModel
        exclude = ('created_at', 'patient')
