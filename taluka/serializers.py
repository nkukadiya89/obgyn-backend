from django.db.models import Q
from rest_framework import serializers

from .models import TalukaModel


class TalukaSerializers(serializers.ModelSerializer):
    def validate(self, data):
        taluka_name = data.get('taluka_name')
        district = data.get('district')
        duplicate_taluka = TalukaModel.objects.filter(deleted=0, taluka_name__iexact=taluka_name, district_id=district)

        if self.partial:
            duplicate_taluka = duplicate_taluka.filter(~Q(pk=self.instance.taluka_id)).first()
        else:
            duplicate_taluka = duplicate_taluka.first()

        if duplicate_taluka != None:
            raise serializers.ValidationError("Taluka already exist.")

        return data

    taluka_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = TalukaModel
        fields = ['taluka_id', 'taluka_name', 'district', 'created_by', 'deleted']
