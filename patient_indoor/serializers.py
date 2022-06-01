from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientIndoorModel, IndoorAdviceModel
from manage_fields.serializers import ManageFieldsSerializers
from advice.serializers import AdviceSerializers
from advice.models import AdviceModel


class PatientIndoorSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientIndoorSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]

        for fld_nm in ["eb_pp", "ps", "pv", "operation","provisional_diagnosis"]:
            fld_name = fld_nm + "_name"
            search_instance = "instance" + "." + fld_nm
            if fld_nm in ret:
                ret[fld_name] = ManageFieldsSerializers(eval(search_instance)).data["field_value"]

        advice = AdviceModel.objects.filter(indooradvicemodel__patient_indoor_id=instance.patient_indoor_id)

        advice = AdviceSerializers(advice, many=True)
        ret["advice_lst"] = advice.data

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

    patient_indoor_id = serializers.IntegerField(read_only=True)
    

    class Meta:
        model = PatientIndoorModel
        exclude = ('created_at', 'patient')


class IndoorAdviceSerializers(serializers.ModelSerializer):

    indoor_advice_id = serializers.IntegerField(read_only=True)
    indoor_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    adm_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    oper_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    disch_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)

    class Meta:
        model = IndoorAdviceModel
        exclude = ('created_at',)
