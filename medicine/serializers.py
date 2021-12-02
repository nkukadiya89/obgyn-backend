from django.db.models import Q
from rest_framework import serializers

from .models import TimingModel, MedicineTypeModel, MedicineModel


class TimingSerializers(serializers.ModelSerializer):
    def validate(self, data):
        timing = data.get('timing')
        language = data.get("language")

        duplicate_timing = TimingModel.objects.filter(deleted=0, timing__iexact=timing, language_id=language)

        if self.partial:
            duplicate_timing = duplicate_timing.filter(~Q(pk=self.instance.timing_id)).first()
        else:
            duplicate_timing = duplicate_timing.first()

        if duplicate_timing != None:
            raise serializers.ValidationError("Timing already exist.")

        return data

    class Meta:
        model = TimingModel
        fields = ['timing_id', 'language', 'timing', 'created_by', 'deleted']


class MedicineTypeSerializers(serializers.ModelSerializer):
    def validate(self, data):
        medicine_type = data.get('medicine_type')
        duplicate_type = MedicineTypeModel.objects.filter(deleted=0, medicine_type__iexact=medicine_type)

        if self.partial:
            duplicate_type = duplicate_type.filter(~Q(pk=self.instance.medicine_type_id)).first()
        else:
            duplicate_type = duplicate_type.first()

        if duplicate_type != None:
            raise serializers.ValidationError("Medicine Type already exist.")

        return data

    class Meta:
        model = MedicineTypeModel
        fields = ['medicine_type_id', 'medicine_type', 'created_by', 'deleted']


class MedicineSerializers(serializers.ModelSerializer):
    class Meta:
        model = MedicineModel
        fields = ['medicine_id', 'barcode', 'medicine_type', 'medicine', 'contain', 'per_day', 'for_day',
                  'total_tablet', 'company', 'morning_timing', 'noon_timing', 'evening_timing', 'bed_timing',
                  'created_by', 'deleted']
