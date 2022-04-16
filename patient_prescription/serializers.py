from django.db.models.query import Q
from rest_framework import serializers

from medicine.models import TimingModel, MedicineTypeModel
from medicine.serializers import MedicineSerializers
from patient.models import PatientModel
from .models import PatientPrescriptionModel


class PatientPrescriptionSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientPrescriptionSerializers, self).to_representation(instance)

        if "medicine" in ret:
            ret["medicine"] = MedicineSerializers(instance.medicine).data
            # ret["medicine_name"] = MedicineSerializers(instance.medicine).data["medicine"]
            # ret["for_day"] = MedicineSerializers(instance.medicine).data["for_day"]
            # ret["per_day"] = MedicineSerializers(instance.medicine).data["per_day"]

            # ret["medicine_type"] = {}
            # medicine_type_id = MedicineSerializers(instance.medicine).data["medicine_type"]
            # if medicine_type_id:
            #     ret["medicine_type"][medicine_type_id] = MedicineTypeModel.objects.get(
            #         pk=medicine_type_id).medicine_type

            # ret["morning_timing"] = {}
            # morning_timing_id = MedicineSerializers(instance.medicine).data["morning_timing"]
            # if morning_timing_id:
            #     ret["morning_timing"][morning_timing_id] = TimingModel.objects.get(pk=morning_timing_id).timing

            # ret["noon_timing"] = {}
            # noon_timing_id = MedicineSerializers(instance.medicine).data["noon_timing"]
            # if noon_timing_id:
            #     ret["noon_timing"][noon_timing_id] = TimingModel.objects.get(pk=noon_timing_id).timing

            # ret["evening_timing"] = {}
            # evening_timing_id = MedicineSerializers(instance.medicine).data["evening_timing"]
            # if evening_timing_id:
            #     ret["evening_timing"][evening_timing_id] = TimingModel.objects.get(pk=evening_timing_id).timing

            # ret["bed_timing"] = {}
            # bed_timing_id = MedicineSerializers(instance.medicine).data["bed_timing"]
            # if bed_timing_id:
            #     ret["bed_timing"][bed_timing_id] = TimingModel.objects.get(pk=bed_timing_id).timing

        return ret

    def validate(self, data):
        medicine = data.get('medicine')
        consultation = data.get('consultation')

        if "regd_no" in data:
            patient = PatientModel.objects.filter(registered_no=data["regd_no"])
            if len(patient) == 0:
                raise serializers.ValidationError("Patient does not exist")
            data["patient_id"] = patient[0].patient_id
        else:
            raise serializers.ValidationError("Patient is missing")

        duplicate_prescription = PatientPrescriptionModel.objects.filter(consultation_id=consultation,
                                                                         medicine_id=medicine, deleted=0)

        if self.partial:
            duplicate_prescription = duplicate_prescription.filter(~Q(pk=self.instance.patient_prescription_id))
        if len(duplicate_prescription) > 0:
            raise serializers.ValidationError("Prescription already exist.")

        return data

    patient_prescription_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientPrescriptionModel
        fields = ['patient_prescription_id', 'regd_no', 'consultation', 'medicine', 'created_by', 'deleted']
