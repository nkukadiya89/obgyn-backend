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
            ret["patient_id"] = patient.data["patient_id"]
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

        patient_delivery = PatientDeliveryModel.objects.filter(
            deleted=0,
            birth_date=data["birth_date"],
            birth_time=data["birth_time"],
            child_name__iexact=data["child_name"],
            patient_id=data["patient_id"],
        )
        if len(patient_delivery) > 1:
            raise serializers.ValidationError("Child already registered.")

        if len(str(data["pin"])) > 6:
            raise serializers.ValidationError("Check value of PIN")

        if 0 >= int(data["current_age"]) > 99:
            raise serializers.ValidationError("Check value of Current Age")

        if 24 >= int(data["weeks"]) > 40:
            raise serializers.ValidationError("Check value of Weeks")

        if 0 > int(data["no_of_delivery"]) > 15:
            raise serializers.ValidationError("Check value of Delivery count.")

        if len(str(data["weight"])) > 4:
            raise serializers.ValidationError("Check value of Weight.")

        return data

    patient_delivery_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientDeliveryModel
        exclude = ("created_at", "patient")


def change_payload(request):
    request.data["delivery_type"] = request.data["delivery_type"].upper()
    request.data["child_gender"] = request.data["child_gender"].upper()
    return request
