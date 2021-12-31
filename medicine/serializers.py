from django.db.models import Q
from rest_framework import serializers

from .models import TimingModel, MedicineTypeModel, MedicineModel


class TimingSerializers(serializers.ModelSerializer):
    def validate(self, data):
        timing = data.get('timing')
        language = data.get("language")

        duplicate_timing = TimingModel.objects.filter(deleted=0, timing__iexact=timing, languageId=language)

        if self.partial:
            duplicate_timing = duplicate_timing.filter(~Q(pk=self.instance.timingId)).first()
        else:
            duplicate_timing = duplicate_timing.first()

        if duplicate_timing != None:
            raise serializers.ValidationError("Timing already exist.")

        return data

    timingId = serializers.IntegerField(read_only=True)

    class Meta:
        model = TimingModel
        fields = ['timingId', 'language', 'timing', 'createdBy', 'deleted']


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

    medicine_type_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = MedicineTypeModel
        fields = ['medicine_type_id', 'medicineType', 'created_by', 'deleted']


class MedicineSerializers(serializers.ModelSerializer):
    def validate(self, data):
        per_day = data.get("per_day", 1)
        for_day = data.get("for_day", 1)

        data["per_day"] = per_day
        data["for_day"] = for_day
        data["total_tablet"] = per_day * for_day

        if "medicine" in data and "morning_timing" in data and "noon_timing" in data and "evening_timing" in data and "bed_timing" in data:
            medicine = data.get("medicine")
            morning_timing = data.get("morning_timing")
            noon_timing = data.get("noon_timing")
            evening_timing = data.get("eveningTiming")
            bed_timing = data.get("bedtiming")
            duplicate_medicin = MedicineModel.objects.filter(deleted=0).filter(deleted=0, medicine__iexact=medicine,
                                                                   morning_timing_id=morning_timing,
                                                                   noon_timing_id=noon_timing,
                                                                   evening_timing_id=evening_timing,
                                                                   bed_timing_id=bed_timing)

            if self.partial:
                duplicate_medicin = duplicate_medicin.filter(~Q(pk=self.instance.medicineId)).first()
            else:
                duplicate_medicin = duplicate_medicin.first()

            if duplicate_medicin != None:
                raise serializers.ValidationError("Medicine already exist.")
        return data

    medicine_id = serializers.CharField(read_only=True)

    class Meta:
        model = MedicineModel
        fields = ['medicine_id', 'barcode', 'medicine_type', 'medicine', 'contain', 'per_day', 'for_day',
                  'total_tablet', 'company', 'morning_timing', 'noon_timing', 'evening_timing', 'bed_timing',
                  'created_by', 'deleted']
