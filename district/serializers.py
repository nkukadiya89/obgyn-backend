from django.db.models import Q
from rest_framework import serializers

from .models import DistrictModel
from state.serializers import StateSerializers
from language.serializers import LanguageSerializers


class DistrictSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(DistrictSerializers,self).to_representation(instance)

        if "state" in ret:
            ret["state_name"] = StateSerializers(instance.state).data["state_name"]

        if "language" in ret:
            ret["language_name"] = LanguageSerializers(instance.language).data["language"]

        return ret

    def validate(self, data):
        district_name = data.get('district_name')

        state = data.get('state')
        duplicate_district = DistrictModel.objects.filter(deleted=0, district_name__iexact=district_name, state_id=state)

        if self.partial:
            duplicate_district = duplicate_district.filter(~Q(pk=self.instance.district_id)).first()
        else:
            duplicate_district = duplicate_district.first()

        if duplicate_district != None:
            raise serializers.ValidationError("District already exist.")

        return data

    district_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = DistrictModel
        fields = ['district_id', 'district_name', 'state', 'language', 'created_by', 'deleted']
