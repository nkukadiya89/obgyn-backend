from django.db.models import Q
from rest_framework import serializers

from .models import AdviseModel


class AdviseSerializers(serializers.ModelSerializer):


    advise_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AdviseModel
        fields = ['advise_id', 'advise', 'advise_for', 'created_by', 'deleted']
