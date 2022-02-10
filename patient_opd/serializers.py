from rest_framework import serializers

from django.db.models.query import Q
from patient.models import PatientModel
from .models import PatientOpdModel
from patient.serializers import PatientSerializers
from city.serializers import CitySerializers
from taluka.serializers import TalukaSerializers
from district.serializers import DistrictSerializers
from state.serializers import StateSerializers


class PatientOpdSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientOpdSerializers, self).to_representation(instance)


        if "regd_no" in ret:
            patient = PatientModel.objects.filter(registered_no=ret["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            ret["patient_id"] = PatientSerializers(instance.patient).data["patient_id"]
            ret["first_name"] = PatientSerializers(instance.patient).data["first_name"]
            ret["middle_name"] = PatientSerializers(instance.patient).data["middle_name"]
            ret["last_name"] = PatientSerializers(instance.patient).data["last_name"]
            ret["phone"] = PatientSerializers(instance.patient).data["phone"]
            ret["department"] = PatientSerializers(instance.patient).data["department"]
            ret["regd_no"] = PatientSerializers(instance.patient).data["registered_no"]
            ret["married"] = PatientSerializers(instance.patient).data["married"]
            ret["patient_type"] = PatientSerializers(instance.patient).data["patient_type"]
            ret["patient_detail"] = PatientSerializers(instance.patient).data["patient_detail"]
            ret["date_of_opd"] = PatientSerializers(instance.patient).data["date_of_opd"]
            ret["husband_father_name"] = PatientSerializers(instance.patient).data["husband_father_name"]
            ret["grand_father_name"] = PatientSerializers(instance.patient).data["grand_father_name"]
            ret["profile_image"] = PatientSerializers(instance.patient).data["profile_image"]
            ret["age"] = PatientSerializers(instance.patient).data["age"]
            ret["taluka"] = PatientSerializers(instance.patient).data["taluka"]
            ret["district"] = PatientSerializers(instance.patient).data["district"]
            ret["city"] = PatientSerializers(instance.patient).data["city"]
            ret["city_name"] = CitySerializers(instance.patient.city).data["city_name"]
            ret["taluka"] = CitySerializers(instance.patient.city).data["taluka"]
            ret["taluka_name"] = TalukaSerializers(instance.patient.city.taluka).data["taluka_name"]
            ret["district"] = TalukaSerializers(instance.patient.city.taluka).data["district"]
            ret["district_name"] = DistrictSerializers(instance.patient.city.taluka.district).data["district_name"]
            ret["state"] = DistrictSerializers(instance.patient.city.taluka.district).data["state"]
            ret["state_name"] = StateSerializers(instance.patient.city.taluka.district.state).data["state_name"]

        return ret
    def validate(self, data):
        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        # patient_opd = PatientOpdModel.objects.filter(opd_date=data["opd_date"], patient_id=data["patient_id"])
        #
        # if self.partial:
        #     patient_opd = patient_opd.filter(~Q(pk=self.instance.patient_opd_id))
        #
        # if len(patient_opd) > 0:
        #     raise serializers.ValidationError("Patient visited today.")

        return data

    patient_opd_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientOpdModel
        exclude = ('created_at', 'patient')
