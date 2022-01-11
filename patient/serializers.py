from django.db.models import Q
from rest_framework import serializers

from .models import PatientModel


class PatientSerializers(serializers.ModelSerializer):
    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone = data.get("phone")
        data["email"] = phone
        data["username"] = phone


        return data

    patient_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientModel
        fields = ['patient_id', 'first_name', 'last_name', 'middle_name', 'password', 'user_type', 'phone', 'state',
                  'city', 'married', 'department', 'patient_type', 'patient_detail', 'date_of_opd', 'registered_no',
                  'grand_parent_name', 'age', 'taluka', 'district', 'created_by', 'deleted']
