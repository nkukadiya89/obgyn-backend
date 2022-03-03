from rest_framework import serializers

from manage_fields.models import ManageFieldsModel
from patient.models import PatientModel
from .models import PatientReferalModel


class PatientReferalSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientReferalSerializers, self).to_representation(instance)

        if "indication" in ret:
            indication_list = []
            for each_indication in ret["indication"]:
                indication = ManageFieldsModel.objects.get(mf_id=each_indication).field_value
                indication_list.append(indication)

            ret["indication_name"] = indication_list

        return ret

    def validate(self, data):
        if "patient_opd_id" not in data:
            raise serializers.ValidationError("OPD is required.")

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
