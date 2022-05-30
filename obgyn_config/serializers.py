from django.db.models import Q
from rest_framework import serializers
from .models import ObgynConfigModel




class Obgyn_Configserializers(serializers.ModelSerializer):

    obgyn_config_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ObgynConfigModel
        fields = fields = "__all__"
