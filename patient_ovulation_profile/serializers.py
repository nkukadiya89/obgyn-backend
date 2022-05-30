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
        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        if len(str(data["right_ovary_mm"])) >4:
            raise serializers.ValidationError("check data for Right ovary value.")

        if len(str(data["left_ovary_mm"])) >4:
            raise serializers.ValidationError("check data for Left ovary value.")
        
        if len(data["endometrium_mm"]) > 4:
            raise serializers.ValidationError("check data for Endometrium value.")

        return data

    patient_ovulation_profile_id = serializers.IntegerField(read_only=True)
    op_date = serializers.DateField(format="%d-%m-%Y")
    

    class Meta:
        model = PatientOvulationProfileModel
        exclude = ('created_at', 'patient')
