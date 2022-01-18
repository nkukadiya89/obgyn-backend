from rest_framework import serializers

from .models import AdviceModel, AdviceGroupModel


class AdviceGroupSerializers(serializers.ModelSerializer):
    advice_group_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AdviceGroupModel
        fields = ['advice_group_id', 'advice_group', 'created_by', 'deleted']


class AdviceSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(AdviceSerializers, self).to_representation(instance)

        if "advice_group" in ret:
            ret['advice_group_name'] = AdviceGroupSerializers(instance.advice_group).data["advice_group"]
        return ret

    advice_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AdviceModel
        fields = ['advice_id', 'advice', 'advice_group', 'advice_for', 'detail', 'created_by', 'deleted']
