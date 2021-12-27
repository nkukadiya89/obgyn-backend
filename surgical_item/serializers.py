from django.db.models import Q
from rest_framework import serializers

from surgical_item.models import SurgicalItemModel, SurgicalItemGroupModel


class SurgicalItemSerializers(serializers.ModelSerializer):

    def validate(self, data):
        drug_name = data.get("drugName")
        duplicate_drug = SurgicalItemModel.objects.filter(deleted=0, drugName__iexact=drug_name)

        if self.partial:
            duplicate_drug = duplicate_drug.filter(~Q(pk=self.instance.surgicalItemId)).first()
        else:
            duplicate_drug = duplicate_drug.first()

        if duplicate_drug != None:
            raise serializers.ValidationError("Drug already exist.")

        return data

    surgicalItemId = serializers.IntegerField(read_only=True)

    class Meta:
        model = SurgicalItemModel
        fields = ['surgicalItemId', 'drugName', 'mrp', 'batchNumber', 'mfgDate', 'expDate', 'user', 'createdBy',
                  'deleted']


class SurgicalItemGroupSerializers(serializers.ModelSerializer):

    def validate(self, data):
        drug_name = data.get("drugName")
        duplicate_drug = SurgicalItemGroupModel.objects.filter(deleted=0, drugName__iexact=drug_name)

        if self.partial:
            duplicate_drug = duplicate_drug.filter(~Q(pk=self.instance.siGroupId)).first()
        else:
            duplicate_drug = duplicate_drug.first()

        if duplicate_drug != None:
            raise serializers.ValidationError("Drug Group already exist.")

        return data

    siGroupId = serializers.IntegerField(read_only=True)

    class Meta:
        model = SurgicalItemGroupModel
        fields = ['siGroupId', 'drugName', 'surgicalItem', 'createdBy', 'deleted']
