from django.db.models import Q
from rest_framework import serializers

from .models import CityModel


class CitySerializers(serializers.ModelSerializer):
    def validate(self, data):
        city_name = data.get('city_name')
        taluka_id = data.get('taluka')
        duplicate_city = CityModel.objects.filter(deleted=0, city_name__iexact=city_name, taluka_id=taluka_id)

        if self.partial:
            duplicate_city = duplicate_city.filter(~Q(pk=self.instance.city_id)).first()
        else:
            duplicate_city = duplicate_city.first()

        if duplicate_city != None:
            raise serializers.ValidationError("City already exist.")

        return data

    city_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CityModel
        fields = ['city_id', 'city_name', 'taluka', 'created_by', 'deleted']
