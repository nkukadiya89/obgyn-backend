from rest_framework import serializers

from manage_fields.serializers import ManageFieldsSerializers
from patient.models import PatientModel
from .models import PatientUSGFormModel, USGFormChildModel


class USGFormChildSerializers(serializers.ModelSerializer):
    usgform_child_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = USGFormChildModel
        exclude = ('created_at',)


class PatientUSGFormSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientUSGFormSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]

        for fld_nm in ["indication", "result_of_sonography", "any_indication_mtp"]:
            fld_name = fld_nm + "_name"
            search_instance = "instance" + "." + fld_nm
            if fld_nm in ret:
                ret[fld_name] = ManageFieldsSerializers(eval(search_instance)).data["field_value"]


        usg_child_list = USGFormChildModel.objects.filter(patient_usgform_id=instance.patient_usgform_id)
        usg_child_lst = []
        for usg_child in usg_child_list:
            usg_childs = {}
            usg_childs["usgform_child_id"] = usg_child.usgform_child_id
            usg_childs["gender"] = usg_child.child_gender
            usg_childs["child_year"] = usg_child.child_year
            usg_childs["child_month"] = usg_child.child_month

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
        exclude = ('created_at', 'patient')
