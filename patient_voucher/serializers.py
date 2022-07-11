from re import T
from rest_framework import serializers
from medicine.models import MedicineModel

from patient.models import PatientModel
from .models import PatientVoucherModel, VoucherItemModel, voucher_type_choice
from surgical_item.models import SurgicalItemModel
from surgical_item.serializers import SurgicalItemSerializers
from medicine.serializers import MedicineSerializers


class PatientVoucherSerializers(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(PatientVoucherSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]
        
        voucher_item = VoucherItemModel.objects.filter(patient_voucher_id=instance.patient_voucher_id)
        voucher_item = VoucherItemSerializers(voucher_item, many=True)

        ret["voucher_type_name"] = [vt[1] for vt in voucher_type_choice if vt[0] == instance.voucher_type][0]
        
        # if "voucher_type" in ret:
        #     ret["voucher_type_name"] = voucher_type_choice[instance.voucher_type]

        ret["surgical_item"] = voucher_item.data
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
    bill_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)

    class Meta:
        model = PatientVoucherModel
        exclude = ('created_at', 'patient')


class VoucherItemSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(VoucherItemSerializers, self).to_representation(instance)

        if "rate" in ret:
            ret["mrp"] = ret["rate"]
            del ret["rate"]
        
        if "voucher_item_id" in ret:
            ret["surgical_item_id"] = ret["voucher_item_id"]
            del ret["voucher_item_id"]

        if "surgical_item" in ret:
            surgical_item = SurgicalItemModel.objects.filter(pk=ret["surgical_item"]).first()
            if surgical_item:
                ret["drug_name"] = surgical_item.drug_name
                ret["batch_number"] = surgical_item.batch_number
                ret["mfg_date"] = surgical_item.mfg_date
                ret["exp_date"] = surgical_item.exp_date
        return ret

    def validate(self, data):
        data["total_amount"] = float(data["unit"]) * float(data["rate"])
        

        return data

    voucher_item_id = serializers.IntegerField(read_only=True)
    total_amount = serializers.FloatField(read_only=True)

    class Meta:
        model = VoucherItemModel
        exclude = ('created_at',)
