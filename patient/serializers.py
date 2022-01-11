from django.db.models import Q
from rest_framework import serializers

from .models import PatientModel


class PatientSerializers(serializers.ModelSerializer):
    # def validate(self, data):
    #     patient_name = data.get('patient_name')
    #     duplicate_patient = PatientModel.objects.filter(deleted=0, patient_name__iexact=patient_name)
    #
    #     if self.partial:
    #         duplicate_patient = duplicate_patient.filter(~Q(pk=self.instance.patient_id)).first()
    #     else:
    #         duplicate_patient = duplicate_patient.first()
    #
    #     if duplicate_patient != None:
    #         raise serializers.ValidationError("Patient already exist.")
    #
    #     return data

    patient_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientModel
        fields = ['patient_id', 'first_name', 'last_name', 'middle_name', 'password', 'user_type', 'phone', 'state',
                  'city', 'married', 'department', 'patient_type', 'patient_detail', 'date_of_opd', 'registered_no',
                  'grand_parent_name', 'age', 'taluka', 'district', 'created_by', 'deleted']
