from re import T
from tkinter.tix import Tree
from jmespath import search
from rest_framework import serializers
import datetime
from diagnosis.serializers import DiagnosisSerializers

from manage_fields.serializers import ManageFieldsSerializers
from patient.models import PatientModel
from .models import ConsultationModel
from patient_prescription.models import PatientPrescriptionModel
from patient_prescription.serializers import PatientPrescriptionSerializers
from medicine.models import MedicineModel
from medicine.serializers import MedicineSerializers


class ConsultationSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(ConsultationSerializers, self).to_representation(instance)

        if "patient_opd" in ret:
            ret["patient_opd_id"] = ret["patient_opd"]
            del ret["patient_opd"]

        if "diagnosis" in ret:
            ret["diagnosis_name"] = DiagnosisSerializers(instance.diagnosis).data[
                "diagnosis_name"
            ]
        
        first_edd =  PatientModel.objects.filter(
            registered_no=instance.regd_no
        ).values("first_edd")[0]["first_edd"]

        if first_edd:
            ret["first_edd"] =first_edd.strftime("%d-%m-%Y")

        for fld_nm in ["co", "ho", "eb_pp", "ps", "pv", "fu","breast"]:
            fld_name = fld_nm + "_name"
            search_instance = "instance" + "." + fld_nm
            if fld_nm in ret:
                ret[fld_name] = ManageFieldsSerializers(eval(search_instance)).data[
                    "field_value"
                ]

        # medicine = PatientPrescriptionModel.objects.filter(consultation_id=instance.consultation_id)
        medicine = MedicineModel.objects.filter(
            patientprescriptionmodel__consultation_id=instance.consultation_id
        )
        medicine = MedicineSerializers(medicine, many=True)
        ret["medicine"] = medicine.data

        return ret

    def validate(self, data):
        
        if data["ut_weeks"]:
            if 4 >= int(data["ut_weeks"]) >= 41:
                raise serializers.ValidationError("Enter valid UT Weeks")

        if data["puls"]:
            if 0 >= int(data["puls"]) >= 200:
                raise serializers.ValidationError("Enter valid Puls")

        if len(data["bp"]) >= 8:
            raise serializers.ValidationError("Enter valid BP")

        if data["tsh"]:
            if len(str(data["tsh"])) >= 8:
                raise serializers.ValidationError("Enter valid TSH")

        if data["resperistion"]:
            if  len(data["resperistion"])>6:
                raise serializers.ValidationError("Enter valid Resperistion")

        if  0 >= int(data["spo2"]) >= 100:
            raise serializers.ValidationError("Enter valid SpO2%")

        if data["mh_every"]:
            if 0 >= int(data["mh_every"]) <= 90:
                raise serializers.ValidationError("mh_every is not in the 0-90 ")    

        if data["mh_for"]:
            if 0 >= int(data["mh_for"]) <= 30:
                raise serializers.ValidationError("mh_for is not in the 0-30 ")        

        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        return data

    consultation_id = serializers.IntegerField(read_only=True)
    patient_type = serializers.CharField(required=True)
    lmp_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    edd_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    possible_lmp = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    possible_edd = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    fu_date = serializers.DateField(format="%d-%m-%Y", allow_null=True)
    first_edd = serializers.DateField(format="%d-%m-%Y", allow_null=True)

    class Meta:
        model = ConsultationModel
        exclude = ("created_at", "patient", "opd_date")
