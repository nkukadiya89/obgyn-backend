from django.db.models import Q
from rest_framework import serializers
from .models import ObgynConfigModel
from city.serializers import CitySerializers
from taluka.serializers import TalukaSerializers
from district.serializers import DistrictSerializers
from state.serializers import StateSerializers
from manage_fields.serializers import ManageFieldsSerializers




class Obgyn_Configserializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(Obgyn_Configserializers,self).to_representation(instance)

        if "city" in ret:
            ret["city_name"] = CitySerializers(instance.city).data["city_name"]
        if "taluka" in ret:
            ret["taluka_name"] = TalukaSerializers(instance.taluka).data["taluka_name"]
        if "district" in ret:
            ret["district_name"] = DistrictSerializers(instance.district).data["district_name"]
        if "state" in ret:
            ret["state_name"] = StateSerializers(instance.state).data["state_name"]
        if "manage_field" in ret:
            ret["manage_field_name"] = ManageFieldsSerializers(instance.manage_field).data["field_value"]

        return ret

    obgyn_config_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ObgynConfigModel
        fields = fields = "__all__"
