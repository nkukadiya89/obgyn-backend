from rest_framework import serializers

from manage_fields.serializers import ManageFieldsSerializers
from patient.models import PatientModel
from manage_fields.models import ManageFieldsModel
from .models import PatientUSGFormModel, USGFormChildModel
from user.serializers import UserSerializers
from datetime import datetime, date
from dateutil.relativedelta import *


class USGFormChildSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(USGFormChildSerializers, self).to_representation(instance)

        if "child_dob" in ret:
            ret["child_year"] = datetime.strptime(ret["child_dob"], "%Y-%m-%d").year
            ret["child_month"] = datetime.strptime(ret["child_dob"], "%Y-%m-%d").month

        return ret

    def validate(self, data):

        data["child_dob"] = (
            date.today()
            + relativedelta(years=-data["child_year"])
            + relativedelta(months=-data["child_month"])
        )
        return data

    usgform_child_id = serializers.IntegerField(read_only=True)
    child_dob = serializers.DateField(read_only=True)
    child_year = serializers.IntegerField()
    child_month = serializers.IntegerField()

    class Meta:
        model = USGFormChildModel
        exclude = ("created_at",)


class PatientUSGFormSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientUSGFormSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]

        if "indication" in ret:
            indication_list = {}
            for each_indication in ret["indication"]:
                indication = ManageFieldsModel.objects.get(mf_id=each_indication)
                indication_list[indication.mf_id] = indication.field_value

            ret["indication_name"] = indication_list

        if "name_of_doctor" in ret:
            ret["name_of_doctor_name"] = (
                UserSerializers(instance.name_of_doctor).data["first_name"].title()
                + " "
                + UserSerializers(instance.name_of_doctor).data["last_name"].title()
            )

        for fld_nm in ["result_of_sonography", "any_indication_mtp", "any_other"]:
            fld_name = fld_nm + "_name"
            search_instance = "instance" + "." + fld_nm
            if fld_nm in ret:
                ret[fld_name] = ManageFieldsSerializers(eval(search_instance)).data[
                    "field_value"
                ]

        usg_child_list = USGFormChildModel.objects.filter(
            patient_usgform_id=instance.patient_usgform_id
        )
        usg_child_lst = []
        for usg_child in usg_child_list:
            usg_childs = {}
            usg_childs["usgform_child_id"] = usg_child.usgform_child_id
            usg_childs["child_gender"] = usg_child.child_gender
            usg_childs["child_year"] = usg_child.child_dob.year
            usg_childs["child_month"] = usg_child.child_dob.month
            
            usg_child_lst.append(usg_childs)

        ret["usg_child"] = usg_child_lst
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

    patient_usgform_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientUSGFormModel
        exclude = ("created_at", "patient")
