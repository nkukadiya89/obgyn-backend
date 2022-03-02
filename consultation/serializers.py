from rest_framework import serializers

from manage_fields.serializers import ManageFieldsSerializers
from patient.models import PatientModel
from .models import ConsultationModel


class ConsultationSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(ConsultationSerializers, self).to_representation(instance)

        for fld_nm in ["eb_pp", "ps", "pv", "advice", "fu"]:
            fld_name = fld_nm + "_name"
            search_instance = "instance" + "." + fld_nm
            if fld_nm in ret:
                ret[fld_name] = ManageFieldsSerializers(eval(search_instance)).data["field_value"]

        return ret

    def validate(self, data):
        if "patient_opd" not in data:
            raise serializers.ValidationError("OPD is required.")

        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        return data

    consultation_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ConsultationModel
        exclude = ('created_at', 'patient')
