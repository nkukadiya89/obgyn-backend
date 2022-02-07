from django.db.models import Q
from rest_framework import serializers
from taluka.serializers import TalukaSerializers
from district.serializers import DistrictSerializers
from state.serializers import StateSerializers

from .models import CityModel


class CitySerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(CitySerializers, self).to_representation(instance)

        if "taluka" in ret:
            ret["taluka_name"] = TalukaSerializers(instance.taluka).data["taluka_name"]
            ret["district_name"] = DistrictSerializers(instance.taluka.district).data["district_name"]
            ret["district"] = DistrictSerializers(instance.taluka.district).data["district_id"]
            ret["state_name"] = StateSerializers(instance.taluka.district.state).data["state_name"]
            ret["state_id"] = StateSerializers(instance.taluka.district.state).data["state_id"]

        return ret

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
