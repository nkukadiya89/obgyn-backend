from django.db.models import Q
from rest_framework import serializers

from diagnosis.models import DiagnosisModel
from medicine.models import MedicineModel


class DiagnosisSerializers(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(DiagnosisSerializers, self).to_representation(instance)

        medicine_name_list = {}
        for medicine1 in ret["medicine"]:
            medicine_name = MedicineModel.objects.get(pk=medicine1)
            medicine_name_list[medicine_name.medicine_id] = medicine_name.medicine

            ret['medicine_name'] = medicine_name_list
            # ret.pop("medicine")

        return ret

    def validate(self, data):
        diagnosis_name = data.get('diagnosis_name', "")
        ut_weeks = data.get("ut_weeks", 0)
        ut_days = data.get("ut_days", 0)
        diagnosis_type = data.get("diagnosis_type")
        created_by = data.get('created_by')

        if diagnosis_type.upper() not in ["D", "U"]:
            raise serializers.ValidationError("Diagnosis type not valid")

        data["diagnosis_type"] = data.get('diagnosis_type').upper()

        if diagnosis_type.upper() == "U":
            if int(data.get('ut_weeks')) <= 0:
                raise serializers.ValidationError(
                    "UT Weeks not provided.")
        elif diagnosis_type.upper() == "D":
            if not diagnosis_name or len(diagnosis_name) == 0:
                raise serializers.ValidationError(
                    "Diagnosis Name not provided.")

        if diagnosis_type == "D":
            duplicate_diagnosis = DiagnosisModel.objects.filter(
                deleted=0, diagnosis_name__iexact=diagnosis_name, created_by=created_by)
        elif diagnosis_type == "U":
            duplicate_diagnosis = DiagnosisModel.objects.filter(
                deleted=0, ut_weeks=ut_weeks, created_by=created_by)

        if self.partial:
            duplicate_diagnosis = duplicate_diagnosis.filter(
                ~Q(pk=self.instance.diagnosis_id)).first()
        else:
            duplicate_diagnosis = duplicate_diagnosis.first()

        if duplicate_diagnosis != None:
            raise serializers.ValidationError("Diagnosis already exist.")

        return data

    diagnosis_id = serializers.IntegerField(read_only=True)
    fu = serializers.IntegerField(source="ut_days")

    # medicine = MedicineSerializers(many=True)
    class Meta:
        model = DiagnosisModel
        fields = ['diagnosis_id', 'diagnosis_type', 'diagnosis_name', 'medicine', 'ut_weeks', 'fu', 'advice',
                  'created_by',
                  'deleted']
