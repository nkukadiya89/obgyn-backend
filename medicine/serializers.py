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

    timingId = serializers.IntegerField(source='timing_id', read_only=True)
    createdBy = serializers.IntegerField(source='created_by')

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

    medicineTypeId = serializers.IntegerField(source='medicine_type_id', read_only=True)
    medicineType = serializers.CharField(source='medicine_type')
    createdBy = serializers.IntegerField(source='created_by')

    class Meta:
        model = MedicineTypeModel
        fields = ['medicineTypeId', 'medicineType', 'createdBy', 'deleted']


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
            evening_timing = data.get("evening_timing")
            bed_timing = data.get("bed_timing")
            duplicate_medicin = MedicineModel.objects.all().filter(deleted=0, medicine__iexact=medicine,
                                                                   morning_timing_id=morning_timing,
                                                                   noon_timing_id=noon_timing,
                                                                   evening_timing_id=evening_timing,
                                                                   bed_timing_id=bed_timing)

            if self.partial:
                duplicate_medicin = duplicate_medicin.filter(~Q(pk=self.instance.medicine_id)).first()
            else:
                duplicate_medicin = duplicate_medicin.first()

            if duplicate_medicin != None:
                raise serializers.ValidationError("Medicine already exist.")
        return data

    medicineId = serializers.CharField(source='medicine_id', read_only=True)
    medicineType = serializers.PrimaryKeyRelatedField(queryset=MedicineTypeModel.objects.all(), many=False,
                                                      source='medicine_type_id')
    perDay = serializers.IntegerField(source='per_day')
    forDay = serializers.IntegerField(source='for_day')
    totalTablet = serializers.IntegerField(source='total_tablet', read_only=True)
    morningTiming = serializers.PrimaryKeyRelatedField(queryset=TimingModel.objects.all(), many=False,
                                                       source='morning_timing_id')
    noonTiming = serializers.PrimaryKeyRelatedField(queryset=TimingModel.objects.all(), many=False,
                                                    source='noon_timing_id')
    eveningTiming = serializers.PrimaryKeyRelatedField(queryset=TimingModel.objects.all(), many=False,
                                                       source='evening_timing_id')
    bedTiming = serializers.PrimaryKeyRelatedField(queryset=TimingModel.objects.all(), many=False,
                                                   source='bed_timing_id')
    createdBy = serializers.IntegerField(source='created_by')

    class Meta:
        model = MedicineModel
        fields = ['medicineId', 'barcode', 'medicineType', 'medicine', 'contain', 'perDay', 'forDay',
                  'totalTablet', 'company', 'morningTiming', 'noonTiming', 'eveningTiming', 'bedTiming',
                  'createdBy', 'deleted']
