from rest_framework import serializers

from manage_fields.models import ManageFieldsModel
from patient.models import PatientModel
from .models import PatientReferalModel
from patient_opd.models import PatientOpdModel


class PatientReferalSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientReferalSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]

        indication_lst = {}
        for indication_id in ret["indication"]:
            field_value = ManageFieldsModel.objects.filter(pk=indication_id).values("field_value")
            indication_lst[indication_id] = field_value[0]["field_value"]

        ret["indication_name"] = indication_lst

        return ret

    def validate(self, data):

        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        if "indication" not in data:
            raise serializers.ValidationError("Indication/S for Diagnostic Procedure is missing")
        return data

    patient_referal_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientReferalModel
        fields = ['patient_referal_id', 'regd_no', 'patient_opd', 'indication', 'created_by', 'deleted']
