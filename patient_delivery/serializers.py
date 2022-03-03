from rest_framework import serializers

from patient.models import PatientModel
from patient.serializers import PatientSerializers
from .models import PatientDeliveryModel


class PatientDeliverySerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientDeliverySerializers, self).to_representation(instance)
        patient = PatientSerializers(instance.patient)
        ret["first_name"] = patient.data["first_name"]
        ret["last_name"] = patient.data["last_name"]
        ret["husband_father_name"] = patient.data["husband_father_name"]
        ret["grand_father_name"] = patient.data["grand_father_name"]
        ret["phone"] = patient.data["phone"]

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

        patient_delivery = PatientDeliveryModel.objects.filter(deleted=0, birth_date=data["birth_date"],
                                                               birth_time=data["birth_time"],
                                                               child_name__iexact=data["child_name"],
                                                               patient_id=data["patient_id"])
        if len(patient_delivery) > 1:
            raise serializers.ValidationError("Child already registered.")

        return data

    patient_delivery_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientDeliveryModel
        exclude = ('created_at', 'patient')
