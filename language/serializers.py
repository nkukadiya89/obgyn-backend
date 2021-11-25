from rest_framework import serializers

from .models import LanguageModel


class LanguageSerializers(serializers.ModelSerializer):
    class Meta:
        model = LanguageModel
        fields = ['language_id', 'language', 'created_by', 'deleted']
