from re import T
from rest_framework import serializers

from manage_fields.serializers import ManageFieldsSerializers
from patient.models import PatientModel
from .models import ConsultationModel
from patient_prescription.models import PatientPrescriptionModel
from patient_prescription.serializers import PatientPrescriptionSerializers



class ConsultationSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(ConsultationSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]

        for fld_nm in ["eb_pp", "ps", "pv", "advice", "fu"]:
            fld_name = fld_nm + "_name"
            search_instance = "instance" + "." + fld_nm
            if fld_nm in ret:
                ret[fld_name] = ManageFieldsSerializers(eval(search_instance)).data["field_value"]

        medicine = PatientPrescriptionModel.objects.filter(consultation_id=instance.consultation_id)

        medicine = PatientPrescriptionSerializers(medicine, many=True)
        ret["medicine"] = medicine.data

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

    consultation_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ConsultationModel
        exclude = ('created_at', 'patient', 'opd_date')
        
