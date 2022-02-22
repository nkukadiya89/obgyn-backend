from rest_framework import serializers

from patient.models import PatientModel
from .models import PatientBillingModel


class PatientBillingSerializers(serializers.ModelSerializer):
    def validate(self, data):
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

    class Meta:
        model = PatientBillingModel
        exclude = ('created_at', 'patient')
