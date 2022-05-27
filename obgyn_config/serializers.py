from django.db.models import Q
from rest_framework import serializers
from .models import ObgynConfigModel
from user.models import User
from manage_fields.models import FieldMasterModel
from state.serializers import StateSerializers
from taluka.serializers import TalukaSerializers
from city.serializers import CitySerializers
from district.serializers import DistrictSerializers


class Obgyn_Configserializers(serializers.ModelSerializer):

    obgyn_config_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ObgynConfigModel
        fields = fields = "__all__"
