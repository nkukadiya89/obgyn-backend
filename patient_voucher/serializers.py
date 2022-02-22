from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientVoucherModel, VoucherItemModel





class PatientVoucherSerializers(serializers.ModelSerializer):
    def validate(self, data):
        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        return data

    patient_voucher_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientVoucherModel
        exclude = ('created_at', 'patient')



class VoucherItemSerializers(serializers.ModelSerializer):
    def validate(self, data):
        data["total_amount"] = float(data["unit"]) * float(data["rate"])

        return data

    voucher_item_id = serializers.IntegerField(read_only=True)
    total_amount = serializers.FloatField(read_only=True)

    class Meta:
        model = VoucherItemModel
        exclude = ('created_at',)
