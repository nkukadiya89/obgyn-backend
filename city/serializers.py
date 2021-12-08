from django.db.models import Q
from rest_framework import serializers

from .models import CityModel


class CitySerializers(serializers.ModelSerializer):
    def validate(self, data):
        city_name = data.get('city_name')
        state = data.get('state')
        duplicate_city = CityModel.objects.filter(deleted=0, city_name__iexact=city_name, state_id=state)

        if self.partial:
            duplicate_city = duplicate_city.filter(~Q(pk=self.instance.city_id)).first()
        else:
            duplicate_city = duplicate_city.first()

        if duplicate_city != None:
            raise serializers.ValidationError("City already exist.")

        return data

    cityId = serializers.IntegerField(source='city_id', read_only=True)
    cityName = serializers.CharField(source='city_name')
    createdBy = serializers.IntegerField(source='created_by')

    class Meta:
        model = CityModel
        fields = ['cityId', 'cityName', 'state', 'createdBy', 'deleted']
