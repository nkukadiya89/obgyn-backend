from rest_framework import serializers

from manage_fields.models import ManageFieldsModel
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

        if "indication" in ret:
            indication_list = []
            for each_indication in ret["indication"]:
                indication = ManageFieldsModel.objects.get(mf_id=each_indication).field_value
                indication_list.append(indication)

            ret["indication_name"] = indication_list

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
