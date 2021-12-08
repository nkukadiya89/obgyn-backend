from django.db.models import Q
from rest_framework import serializers

from manage_fields.models import ManageFieldsModel


class ManageFieldsSerializers(serializers.ModelSerializer):

    def validate(self, data):
        field_name = data.get("field_name")
        duplicate_manage_fields = ManageFieldsModel.objects.filter(deleted=0, field_name__iexact=field_name)

        language_id = data.get('language', None)
        if language_id != None:
            duplicate_manage_fields = duplicate_manage_fields.filter(language_id=language_id)

        if self.partial:
            duplicate_manage_fields = duplicate_manage_fields.filter(~Q(pk=self.instance.mf_id)).first()
        else:
            duplicate_manage_fields = duplicate_manage_fields.first()

        if duplicate_manage_fields != None:
            raise serializers.ValidationError("This Field already exist.")

        return data

    mfId = serializers.IntegerField(source='mf_id', read_only=True)
    fieldName = serializers.CharField(source='field_name')
    fieldValue = serializers.CharField(source='field_value')
    createdBy = serializers.IntegerField(source='created_by')

    class Meta:
        model = ManageFieldsModel
        fields = ['mfId', 'language', 'fieldName', 'fieldValue', 'createdBy', 'deleted']
