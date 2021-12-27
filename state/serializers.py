from django.db.models import Q
from rest_framework import serializers

from .models import StateModel


class StateSerializers(serializers.ModelSerializer):
    def validate(self, data):
        state_name = data.get('stateName')
        duplicate_state = StateModel.objects.filter(deleted=0, stateName__iexact=state_name)

        if self.partial:
            duplicate_state = duplicate_state.filter(~Q(pk=self.instance.stateId)).first()
        else:
            duplicate_state = duplicate_state.first()

        if duplicate_state != None:
            raise serializers.ValidationError("State already exist.")

        return data

    stateId = serializers.IntegerField(read_only=True)

    class Meta:
        model = StateModel
        fields = ['stateId', 'stateName', 'createdBy', 'deleted']
