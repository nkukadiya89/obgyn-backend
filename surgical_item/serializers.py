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

    surgicalItemId = serializers.IntegerField(source='surgical_item_id',read_only=True)
    drugName = serializers.CharField(source='drug_name')
    batchNumber = serializers.CharField(source='batch_number')
    mfgDate = serializers.CharField(source='mfg_date')
    expDate = serializers.CharField(source='exp_date')
    createdBy = serializers.IntegerField(source='created_by')

    class Meta:
        model = SurgicalItemModel
        fields = ['surgicalItemId', 'drugName', 'mrp', 'batchNumber', 'mfgDate', 'expDate', 'user', 'createdBy',
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

    siGroupId = serializers.IntegerField(source='si_group_id', read_only=True)
    drugName = serializers.CharField(source='drug_name')
    surgicalItem = serializers.IntegerField(source='surgical_item')
    createdBy = serializers.IntegerField(source='created_by')

    class Meta:
        model = SurgicalItemGroupModel
        fields = ['siGroupId', 'drugName', 'surgicalItem', 'createdBy', 'deleted']
