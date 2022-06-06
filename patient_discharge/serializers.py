from rest_framework import serializers

from advice.serializers import AdviceSerializers
from diagnosis.serializers import DiagnosisSerializers
from patient.models import PatientModel
from .models import PatientDischargeModel
from django.db.models.query import Q
from manage_fields.serializers import ManageFieldsSerializers


class PatientDischargeSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientDischargeSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]

        if "diagnosis" in ret:
            ret["diagnosis_name"] = DiagnosisSerializers(instance.diagnosis).data["diagnosis_name"]

        for fld_nm in ["advice", "complain_of", "name_of_operation"]:
            fld_name = fld_nm + "_name"
            search_instance = "instance" + "." + fld_nm
            if fld_nm in ret:
                ret[fld_name] = ManageFieldsSerializers(eval(search_instance)).data["field_value"]

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

    patient_discharge_id = serializers.IntegerField(read_only=True)
    admission_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    ot_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    discharge_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    

    class Meta:
        model = PatientDischargeModel
        exclude = ('created_at', 'patient')
