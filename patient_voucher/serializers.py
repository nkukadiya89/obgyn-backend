from re import T
from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientVoucherModel, VoucherItemModel
from surgical_item.models import SurgicalItemModel
from surgical_item.serializers import SurgicalItemSerializers


class PatientVoucherSerializers(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(PatientVoucherSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]
        
        # surgical_item = SurgicalItemModel.objects.filter(voucheritemmodel__patient_voucher_id=instance.patient_voucher_id)
        # surgical_item = SurgicalItemSerializers(surgical_item,many=True)
        # ret["surgical_item"] = surgical_item.data

        voucher_item = VoucherItemModel.objects.filter(patient_voucher_id=instance.patient_voucher_id)
        voucher_item = VoucherItemSerializers(voucher_item, many=True)
        ret["voucher_item"] = voucher_item.data
        return ret

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
    def to_representation(self, instance):
        ret = super(VoucherItemSerializers, self).to_representation(instance)

        surgical_item = SurgicalItemModel.objects.filter(voucheritemmodel__voucher_item_id=instance.voucher_item_id)
        surgical_item = SurgicalItemSerializers(surgical_item,many=True)
        ret["surgical_item"] = surgical_item.data

        return ret

    def validate(self, data):
        data["total_amount"] = float(data["unit"]) * float(data["rate"])
        

        return data

    voucher_item_id = serializers.IntegerField(read_only=True)
    total_amount = serializers.FloatField(read_only=True)

    class Meta:
        model = VoucherItemModel
        exclude = ('created_at',)
