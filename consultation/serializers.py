from rest_framework import serializers

from manage_fields.serializers import ManageFieldsSerializers
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
        return data

    consultation_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ConsultationModel
        exclude = ('created_at', 'patient')
