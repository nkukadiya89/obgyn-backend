from rest_framework import serializers

from patient.models import PatientModel
from patient.serializers import PatientSerializers
from .models import PatientDeliveryModel
from city.serializers import CitySerializers
from taluka.serializers import TalukaSerializers
from district.serializers import DistrictSerializers
from state.serializers import StateSerializers
from manage_fields.serializers import ManageFieldsSerializers


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

        if "city" in ret:
            ret["city_name"] = CitySerializers(instance.city).data[
                "city_name"
            ]
        if "taluka" in ret:
            ret["taluka_name"] = TalukaSerializers(instance.taluka).data[
                "taluka_name"
            ]
            
        if "district" in ret:
            ret["district_name"] = DistrictSerializers(instance.district).data[
                "district_name"
            ]
        if "state" in ret:
            ret["state_name"] = StateSerializers(instance.state).data[
                "state_name"
            ]

        # if "mother_occupation" in ret:
        #     ret["mother_occupation_name"] = ManageFieldsSerializers(instance.mother_occupation).data["field_value"]
        # if "mother_education" in ret:
        #     ret["mother_education_name"] = ManageFieldsSerializers(instance.mother_education).data["field_value"]
        #
        #
        # if "father_occupation" in ret:
        #     ret["father_occupation_name"] = ManageFieldsSerializers(instance.father_occupation).data["field_value"]
        # if "father_education" in ret:
        #     ret["father_education_name"] = ManageFieldsSerializers(instance.father_education).data["field_value"]

        for fld_nm in ["religion", "episio_by", "dayan", "mother_occupation", "father_occupation", "mother_education","father_education"]:
            fld_name = fld_nm + "_name"
            search_instance = "instance" + "." + fld_nm
            if fld_nm in ret:
                ret[fld_name] = ManageFieldsSerializers(eval(search_instance)).data[
                    "field_value"
                ]

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
    birth_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)

    class Meta:
        model = PatientDeliveryModel
        exclude = ("created_at", "patient")


def change_payload(request):
    request.data["delivery_type"] = request.data["delivery_type"].upper()
    request.data["child_gender"] = request.data["child_gender"].upper()
    return request
