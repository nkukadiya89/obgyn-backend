from rest_framework import serializers

from .models import AdviceModel, AdviceGroupModel


class AdviceSerializers(serializers.ModelSerializer):
    advice_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AdviceModel
        fields = ['advice_id', 'advice', 'advice_for', 'detail', 'created_by', 'deleted']


class AdviceGroupSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(AdviceGroupSerializers, self).to_representation(instance)

        if "advice" in ret:
            ret['advice_name'] = AdviceSerializers(instance.advice).data["advice"]
        return ret

    advice_group_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AdviceGroupModel
        fields = ['advice_group_id', 'advice', 'advice_group', 'created_by', 'deleted']
