from rest_framework import serializers

from state.models import StateModel
from .models import CityModel


class CitySerializers(serializers.ModelSerializer):
    state = serializers.PrimaryKeyRelatedField(queryset=StateModel.objects.all(), many=False)

    class Meta:
        model = CityModel
        fields = ['city_id', 'city_name', 'state', 'created_by', 'deleted']
