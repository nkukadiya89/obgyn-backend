from django.db.models import Q
from rest_framework import serializers

from surgical_item.models import SurgicalItemModel, SurgicalItemGroupModel


class SurgicalItemSerializers(serializers.ModelSerializer):

    def validate(self, data):
        drug_name = data.get("drug_name")
        duplicate_drug = SurgicalItemModel.objects.filter(deleted=0, drug_name__iexact=drug_name)

        if self.partial:
            duplicate_drug = duplicate_drug.filter(~Q(pk=self.instance.surgical_item_id)).first()
        else:
            duplicate_drug = duplicate_drug.first()

        if duplicate_drug != None:
            raise serializers.ValidationError("Drug already exist.")

        return data

    surgical_item_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SurgicalItemModel
        fields = ['surgical_item_id', 'drug_name', 'mrp', 'batch_number', 'mfg_date', 'exp_date', 'user', 'created_by',
                  'deleted']


class SurgicalItemGroupSerializers(serializers.ModelSerializer):

    def validate(self, data):
        drug_name = data.get("drug_name")
        duplicate_drug = SurgicalItemGroupModel.objects.filter(deleted=0, drug_name__iexact=drug_name)

        if self.partial:
            duplicate_drug = duplicate_drug.filter(~Q(pk=self.instance.si_group_id)).first()
        else:
            duplicate_drug = duplicate_drug.first()

        if duplicate_drug != None:
            raise serializers.ValidationError("Drug Group already exist.")

        return data

    siGroup_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SurgicalItemGroupModel
        fields = ['siGroup_id', 'drug_name', 'surgical_item', 'created_by', 'deleted']
