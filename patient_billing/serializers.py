from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientBillingModel


class PatientBillingSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientBillingSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]
        return ret

    def validate(self, data):
        if "patient_opd_id" not in data:
            raise serializers.ValidationError("OPD is required.")

        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        data["total_rs"] = float(data["rs_per_visit"]) + float(data["consulting_fees"]) + float(
            data["rs_per_usg"]) + float(data["usg_rs"]) + float(data["rs_per_room"]) + float(
            data["room_rs"]) + float(data["operative_charge_rs"]) + float(data["medicine_rs"]) + float(
            data["rs_per_day"]) + float(data["nursing_rs"]) + float(data["other_charge"]) + float(
            data["other_rs"])

        return data

    patient_billing_id = serializers.IntegerField(read_only=True)
    total_rs = serializers.IntegerField(read_only=True)
    admission_date = serializers.DateField(format="%d-%m-%Y")
    ot_date = serializers.DateField(format="%d-%m-%Y")
    discharge_date = serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = PatientBillingModel
        exclude = ('created_at', 'patient')
