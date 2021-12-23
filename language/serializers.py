from django.db.models import Q
from rest_framework import serializers

from .models import LanguageModel


class LanguageSerializers(serializers.ModelSerializer):
    def validate(self, data):
        language = data.get('language')
        duplicate_language = LanguageModel.objects.filter(deleted=0, language__iexact=language)

        if self.partial:
            duplicate_language = duplicate_language.filter(~Q(pk=self.instance.language_id)).first()
        else:
            duplicate_language = duplicate_language.first()

        if duplicate_language != None:
            raise serializers.ValidationError("Language already exist.")

        return data

    languageId = serializers.IntegerField(source='language_id', read_only=True)
    createdBy = serializers.IntegerField(source='created_by')

    class Meta:
        model = LanguageModel
        fields = ['languageId', 'language', 'code', 'createdBy', 'deleted']
