from rest_framework import serializers

from manage_fields.serializers import ManageFieldsSerializers
from patient.models import PatientModel
from .models import ConsultationModel


class ConsultationSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(ConsultationSerializers, self).to_representation(instance)

        for fld_nm in ["ho", "co", "temprature", "puls", "bp", "resperistion", "spo2", "pallor", "lcterus", "oedema",
                       "rs", "cvs", "breast", "pv", "tt", "blood_group", "urine_sugar", "urine_protein", "hiv", "hbsag",
                       "vdrl"]:
            fld_name = fld_nm + "_name"
            search_instance = "instance" + "." + fld_nm
            if fld_nm in ret:
                ret[fld_name] = ManageFieldsSerializers(eval(search_instance)).data["field_value"]

        return ret

    def validate(self, data):
        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id

        return data

    consultation_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ConsultationModel
        exclude = ('created_at', 'patient')
