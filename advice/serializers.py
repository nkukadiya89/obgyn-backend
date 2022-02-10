from django.db.models.query import Q
from rest_framework import serializers

from .models import AdviceModel, AdviceGroupModel


class AdviceSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(AdviceSerializers, self).to_representation(instance)

        if "advice_group" in ret:
            ret['advice_group_name'] = AdviceGroupSerializers(instance.advice_group).data["advice_group"]
        return ret

    def validate(self, data):
        advice = data.get('advice')

        duplicate_advice = AdviceModel.objects.filter(advice=advice, deleted=0)

        if self.partial:
            duplicate_advice = duplicate_advice.filter(~Q(pk=self.instance.advice_id)).first()
        else:
            duplicate_advice = duplicate_advice.first()

        if duplicate_advice != None:
            raise serializers.ValidationError("Advice already exist.")

    advice_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AdviceModel
        fields = ['advice_id', 'advice', 'advice_for', 'detail', 'created_by', 'deleted', 'created_at']


class AdviceGroupSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(AdviceGroupSerializers, self).to_representation(instance)

        advice_name_list = []
        for advice1 in ret["advice"]:
            advice = AdviceModel.objects.get(pk=advice1).advice
            advice_name_list.append(advice)
            ret['advice_name'] = advice_name_list

        return ret

    def validate(self, data):
        advice_group = data.get('advice_group')

        duplicate_advice_group = AdviceGroupModel.objects.filter(advice_group=advice_group, deleted=0)

        if self.partial:
            duplicate_advice_group = duplicate_advice_group.filter(~Q(pk=self.instance.advice_group_id)).first()
        else:
            duplicate_advice_group = duplicate_advice_group.first()

        if duplicate_advice_group != None:
            raise serializers.ValidationError("Advice Group already exist.")
        
        return data
    advice_group_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AdviceGroupModel
        fields = ['advice_group_id', 'advice', 'advice_group', 'created_by', 'deleted', 'created_at']
