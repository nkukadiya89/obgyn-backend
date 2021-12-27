from django.db.models import Q
from rest_framework import serializers

from .models import CityModel


class CitySerializers(serializers.ModelSerializer):
    def validate(self, data):
        cityName = data.get('cityName')
        state = data.get('state')
        duplicate_city = CityModel.objects.filter(deleted=0, cityName__iexact=cityName, stateId=state)

        if self.partial:
            duplicate_city = duplicate_city.filter(~Q(pk=self.instance.cityId)).first()
        else:
            duplicate_city = duplicate_city.first()

        if duplicate_city != None:
            raise serializers.ValidationError("City already exist.")

        return data

    cityId = serializers.IntegerField(read_only=True)

    class Meta:
        model = CityModel
        fields = ['cityId', 'cityName', 'state', 'createdBy', 'deleted']
