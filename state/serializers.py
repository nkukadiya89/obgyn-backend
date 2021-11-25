from rest_framework import serializers

from .models import StateModel


class StateSerializers(serializers.ModelSerializer):
    class Meta:
        model = StateModel
        fields = ['state_id', 'state_name', 'created_by', 'deleted']
