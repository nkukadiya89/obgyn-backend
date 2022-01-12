from django.db.models import Q
from rest_framework import serializers

from manage_fields.models import ManageFieldsModel
from language.serializers import LanguageSerializers


class ManageFieldsSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(ManageFieldsSerializers, self).to_representation(instance)

        if "language" in ret:
            ret['language'] = LanguageSerializers(instance.language).data["language"]
            ret['language_id'] = LanguageSerializers(instance.language).data["language_id"]
        return ret


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

    mf_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ManageFieldsModel
        fields = ['mf_id', 'language', 'field_name', 'field_value', 'created_by', 'deleted']
