from django.db.models import Q
from rest_framework import serializers
from language.serializers import LanguageSerializers
from state.serializers import StateSerializers

from .models import TemplateHeaderModel


class TemplateHeaderSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(TemplateHeaderSerializers, self).to_representation(instance)

        if "language" in ret:
            ret["language_name"] = LanguageSerializers(instance.language).data["code"]
        return ret

    def validate(self, data):
        template_header_name = data.get('template_header_name')
        language_id = data.get('language_id')
        duplicate_template_header = TemplateHeaderModel.objects.filter(deleted=0, template_header_name__iexact=template_header_name, language_id=language_id)

        if self.partial:
            duplicate_template_header = duplicate_template_header.filter(~Q(pk=self.instance.template_header_id)).first()
        else:
            duplicate_template_header = duplicate_template_header.first()

        if duplicate_template_header != None:
            raise serializers.ValidationError("TemplateHeader already exist.")

        return data

    template_header_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = TemplateHeaderModel
        exclude = ('created_at',)
