from django.db.models import Q
from rest_framework import serializers

from language.serializers import LanguageSerializers
from manage_fields.models import ManageFieldsModel, FieldMasterModel


class FieldMasterSerializers(serializers.ModelSerializer):
    field_master_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = FieldMasterModel
        fields = ['field_master_id', 'field_master_name', 'created_by', 'deleted']


class ManageFieldsSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(ManageFieldsSerializers, self).to_representation(instance)

        if "field_master" in ret:
            ret["field_master_name"] = FieldMasterSerializers(instance.field_master).data["field_master_name"]

        if "language" in ret:
            ret['language_name'] = LanguageSerializers(instance.language).data["code"]
        return ret

    mf_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ManageFieldsModel
        fields = ['mf_id', 'language', 'field_master', 'field_value', 'created_by', 'deleted']
