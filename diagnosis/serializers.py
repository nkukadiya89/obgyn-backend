from django.db.models import Q
from rest_framework import serializers

from diagnosis.models import DiagnosisModel
from medicine.models import MedicineModel
from medicine.serializers import MedicineSerializers


class DiagnosisSerializers(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(DiagnosisSerializers, self).to_representation(instance)

        medicine_name_list=[]
        for medicine1 in ret["medicine"]:
            medicine_name = MedicineModel.objects.get(pk=medicine1).medicine
            medicine_name_list.append(medicine_name)
            ret['medicine_name'] = medicine_name_list

        return ret

    diagnosis_id = serializers.IntegerField(read_only=True)
    # medicine = MedicineSerializers(many=True)
    class Meta:
        model = DiagnosisModel
        fields = ['diagnosis_id', 'diagnosis_name', 'medicine', 'ut_weeks', 'ut_days', 'created_by', 'deleted']
