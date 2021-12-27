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
        medicine_type = data.get('medicineType')
        duplicate_type = MedicineTypeModel.objects.filter(deleted=0, medicineType__iexact=medicine_type)

        if self.partial:
            duplicate_type = duplicate_type.filter(~Q(pk=self.instance.medicineTypeId)).first()
        else:
            duplicate_type = duplicate_type.first()

        if duplicate_type != None:
            raise serializers.ValidationError("Medicine Type already exist.")

        return data

    medicineTypeId = serializers.IntegerField(read_only=True)

    class Meta:
        model = MedicineTypeModel
        fields = ['medicineTypeId', 'medicineType', 'createdBy', 'deleted']


class MedicineSerializers(serializers.ModelSerializer):
    def validate(self, data):
        per_day = data.get("perDay", 1)
        for_day = data.get("forDay", 1)

        data["perDay"] = per_day
        data["forDay"] = for_day
        data["totalTablet"] = per_day * for_day

        if "medicine" in data and "morningTiming" in data and "noonTiming" in data and "eveningTiming" in data and "bedTiming" in data:
            medicine = data.get("medicine")
            morning_timing = data.get("morningTiming")
            noon_timing = data.get("noonTiming")
            evening_timing = data.get("eveningTiming")
            bed_timing = data.get("bedTiming")
            duplicate_medicin = MedicineModel.objects.all().filter(deleted=0, medicine__iexact=medicine,
                                                                   morningTimingId=morning_timing,
                                                                   noonTimingId=noon_timing,
                                                                   eveningTimingId=evening_timing,
                                                                   bedTimingId=bed_timing)

            if self.partial:
                duplicate_medicin = duplicate_medicin.filter(~Q(pk=self.instance.medicineId)).first()
            else:
                duplicate_medicin = duplicate_medicin.first()

            if duplicate_medicin != None:
                raise serializers.ValidationError("Medicine already exist.")
        return data

    medicineId = serializers.CharField(read_only=True)

    class Meta:
        model = MedicineModel
        fields = ['medicineId', 'barcode', 'medicineType', 'medicine', 'contain', 'perDay', 'forDay',
                  'totalTablet', 'company', 'morningTiming', 'noonTiming', 'eveningTiming', 'bedTiming',
                  'createdBy', 'deleted']
