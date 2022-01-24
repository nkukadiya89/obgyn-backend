from rest_framework import serializers
from django.db.models.query import Q

from diagnosis.serializers import DiagnosisSerializers
from medicine.models import MedicineModel
from patient.models import PatientModel
from .models import PatientPrescriptionModel
from medicine.models import TimingModel, MedicineTypeModel


class PatientPrescriptionSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientPrescriptionSerializers, self).to_representation(instance)

        if "diagnosis" in ret:
            ret["diagnosis_name"] = DiagnosisSerializers(instance.diagnosis).data["diagnosis_name"]
            medicine = DiagnosisSerializers(instance.diagnosis).data["medicine"]
            medicine_name_list = []
            for medicine1 in medicine:
                ret_medicine = {}
                ret_medicine["medicine_name"] = MedicineModel.objects.get(pk=medicine1).medicine
                ret_medicine["for_day"] = MedicineModel.objects.get(pk=medicine1).for_day
                ret_medicine["per_day"] = MedicineModel.objects.get(pk=medicine1).per_day

                medicine_type_id = MedicineModel.objects.get(pk=medicine1).medicine_type_id
                try:
                    ret_medicine["medicine_type"] = medicine_type_id
                    ret_medicine["medicine_type_name"] = MedicineTypeModel.objects.get(pk=medicine_type_id).medicine_type
                except:
                    ret_medicine["medicine_type"] = None
                    ret_medicine["medicine_type_name"] = None

                try:
                    morning_timing_id = MedicineModel.objects.get(pk=medicine1).morning_timing_id
                    ret_medicine["morning_timing"] = morning_timing_id
                    ret_medicine["morning_timing_name"] = TimingModel.objects.get(pk=morning_timing_id).timing
                except:
                    ret_medicine["morning_timing"] = None
                    ret_medicine["morning_timing_name"] = None

                try:
                    noon_timing_id = MedicineModel.objects.get(pk=medicine1).noon_timing_id
                    ret_medicine["noon_timing"] = noon_timing_id
                    ret_medicine["noon_timing_name"] = TimingModel.objects.get(pk=noon_timing_id).timing
                except:
                    ret_medicine["noon_timing"] = None
                    ret_medicine["noon_timing_name"] = None

                try:
                    evening_timing_id = MedicineModel.objects.get(pk=medicine1).evening_timing_id
                    ret_medicine["evening_timing"] = evening_timing_id
                    ret_medicine["evening_timing_name"] = TimingModel.objects.get(pk=evening_timing_id).timing
                except:
                    ret_medicine["evening_timing"] = None
                    ret_medicine["evening_timing_name"] = None

                try:
                    bed_timing_id = MedicineModel.objects.get(pk=medicine1).bed_timing_id
                    ret_medicine["bed_timing"] = bed_timing_id
                    ret_medicine["bed_timing_name"] = TimingModel.objects.get(pk=bed_timing_id).timing
                except:
                    ret_medicine["bed_timing"] = None
                    ret_medicine["bed_timing_name"] = None

                medicine_name_list.append(ret_medicine)

                ret['medicine_name'] = medicine_name_list
                ret_medicine["total_tablet"] = MedicineModel.objects.get(pk=medicine1).total_tablet

        return ret

    def validate(self, data):
        diagnosis = data.get('diagnosis')
        consultation = data.get('consultation')

        patient = PatientModel.objects.filter(registered_no=data["regd_no"])
        if len(patient) == 0:
            raise serializers.ValidationError("Patient does not exist")
        data["patient_id"] = patient[0].patient_id

        duplicate_prescription = PatientPrescriptionModel.objects.filter(consultation_id=consultation,
                                                                         diagnosis_id=diagnosis, deleted=0)

        if self.partial:
            duplicate_prescription = duplicate_prescription.filter(~Q(pk=self.instance.patient_prescription_id))
        if len(duplicate_prescription) > 0:
            raise serializers.ValidationError("Prescription already exist.")


        return data

    patient_prescription_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientPrescriptionModel
        fields = ['patient_prescription_id', 'regd_no', 'consultation', 'diagnosis', 'created_by', 'deleted']
