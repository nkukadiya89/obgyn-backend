from django.db.models import Q
from rest_framework import serializers

from diagnosis.models import DiagnosisModel


class DiagnosisSerializers(serializers.ModelSerializer):

    def validate(self, data):
        diagnosis_name = data.get("diagnosisName")
        duplicate_diagnosis = DiagnosisModel.objects.filter(deleted=0, diagnosisName__iexact=diagnosis_name)

        if self.partial:
            duplicate_diagnosis = duplicate_diagnosis.filter(~Q(pk=self.instance.diagnosisId)).first()
        else:
            duplicate_diagnosis = duplicate_diagnosis.first()

        if duplicate_diagnosis != None:
            raise serializers.ValidationError("Diagnosis already exist.")

        return data

    diagnosisId = serializers.IntegerField(read_only=True)

    class Meta:
        model = DiagnosisModel
        fields = ['diagnosisId', 'diagnosisName', 'medicine', 'createdBy', 'deleted']
