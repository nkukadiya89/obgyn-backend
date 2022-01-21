from rest_framework import serializers

from .models import AdviceModel, AdviceGroupModel



class AdviceSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(AdviceSerializers, self).to_representation(instance)

        if "advice_group" in ret:
            ret['advice_group_name'] = AdviceGroupSerializers(instance.advice_group).data["advice_group"]
        return ret

    advice_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AdviceModel
        fields = ['advice_id', 'advice', 'advice_for', 'detail', 'created_by', 'deleted']


class AdviceGroupSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(AdviceGroupSerializers, self).to_representation(instance)

        advice_name_list = []
        advice_id_list = []
        for advice1 in ret["advice"]:
            advice = AdviceModel.objects.get(pk=advice1)
            advice_name_list.append(advice.advice)
            advice_id_list.append(str(advice.advice_id))
            ret['advice_name'] = advice_name_list
            ret['advice'] = advice_id_list

        return ret

    advice_group_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AdviceGroupModel
        fields = ['advice_group_id','advice', 'advice_group', 'created_by', 'deleted']

