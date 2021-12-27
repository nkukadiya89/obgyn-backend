from django.db.models import Q
from rest_framework import serializers

from manage_fields.models import ManageFieldsModel


class ManageFieldsSerializers(serializers.ModelSerializer):

    def validate(self, data):
        field_name = data.get("fieldName")
        duplicate_manage_fields = ManageFieldsModel.objects.filter(deleted=0, fieldName__iexact=field_name)

        language_id = data.get('language', None)
        if language_id != None:
            duplicate_manage_fields = duplicate_manage_fields.filter(languageId=language_id)

        if self.partial:
            duplicate_manage_fields = duplicate_manage_fields.filter(~Q(pk=self.instance.mfId)).first()
        else:
            duplicate_manage_fields = duplicate_manage_fields.first()

        if duplicate_manage_fields != None:
            raise serializers.ValidationError("This Field already exist.")

        return data

    mfId = serializers.IntegerField(read_only=True)

    class Meta:
        model = ManageFieldsModel
        fields = ['mfId', 'language', 'fieldName', 'fieldValue', 'createdBy', 'deleted']
