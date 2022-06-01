from datetime import datetime

from rest_framework import serializers

from manage_fields.serializers import ManageFieldsSerializers
from patient.models import PatientModel
from .models import PatientOpdModel


class PatientOpdSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientOpdSerializers, self).to_representation(instance)
        if "regd_no" in ret:
            patient = PatientModel.objects.filter(registered_no=str(ret["regd_no"])).select_related(
                'name_title').select_related('husband_title').select_related('grand_title').select_related(
                'taluka').select_related('district').select_related('state').select_related('city')
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")

            ret["opd_date"] = instance.opd_date
            ret["patient_id"] = patient[0].patient_id
            ret["first_name"] = patient[0].first_name
            ret["middle_name"] = patient[0].middle_name
            ret["last_name"] = patient[0].last_name
            ret["phone"] = patient[0].phone if "F_" not in patient[0].phone else ""
            ret["regd_no"] = patient[0].registered_no
            ret["married"] = patient[0].married
            ret["date_of_opd"] = patient[0].date_of_opd
            ret["husband_father_name"] = patient[0].husband_father_name
            ret["grand_father_name"] = patient[0].grand_father_name

            ret['name_title'] = patient[0].name_title_id
            ret['husband_title'] = patient[0].husband_title_id
            ret['grand_title'] = patient[0].grand_title_id
            ret["landmark"] = patient[0].landmark

            ret['name_title_name'] = ManageFieldsSerializers(patient[0].name_title).data["field_value"]
            ret['husband_title_name'] = ManageFieldsSerializers(patient[0].husband_title).data["field_value"]
            ret['grand_title_name'] = ManageFieldsSerializers(patient[0].grand_title).data["field_value"]

            ret["profile_image"] = patient[0].profile_image
            ret["age"] = patient[0].age
            try:
                ret["taluka"] = patient[0].taluka.taluka_id
                ret["taluka_name"] = patient[0].taluka.taluka_name
            except:
                ret["taluka"] = ""
                ret["taluka_name"] = ""
            
            try:
                ret["district"] = patient[0].district.district_id
                ret["district_name"] = patient[0].district.district_name
            except:
                ret["district"] =""
                ret["district_name"] = ""
            
            try:
                ret["city"] = patient[0].city.city_id
                ret["city_name"] = patient[0].city.city_name
            except:
                ret["city"] = ""
                ret["city_name"] = ""

            try:
                ret["state"] = patient[0].state.state_id
                ret["state_name"] = patient[0].state.state_name
            except:
                ret["state"] = ""
                ret["state_name"] = ""

            ret["user_code"] = patient[0].user_code

        return ret

    def validate(self, data):
        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        return data

    patient_opd_id = serializers.IntegerField(read_only=True)
    opd_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)

    class Meta:
        model = PatientOpdModel
        exclude = ('created_at', 'patient')
