from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientOpdModel


class PatientOpdSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientOpdSerializers, self).to_representation(instance)

        if "regd_no" in ret:
            patient = PatientModel.objects.filter(registered_no=ret["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            ret["patient_id"] = patient[0].patient_id
            ret["first_name"] = patient[0].first_name
            ret["middle_name"] = patient[0].middle_name
            ret["last_name"] = patient[0].last_name
            ret["phone"] = patient[0].phone
            ret["department"] = patient[0].department
            ret["regd_no"] = patient[0].registered_no
            ret["grand_father_name"] = patient[0].grand_father_name

        return ret
    def validate(self, data):
        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        patient_opd = PatientOpdModel.objects.filter(opd_date=data["opd_date"], patient_id=data["patient_id"])
        if len(patient_opd) > 0:
            raise serializers.ValidationError("Patient visited today.")

        return data

    patient_opd_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientOpdModel
        exclude = ('created_at', 'patient')
