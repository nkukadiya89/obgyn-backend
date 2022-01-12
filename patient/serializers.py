import random
import string

from rest_framework import serializers

from city.serializers import CitySerializers
from state.serializers import StateSerializers
from .models import PatientModel


class PatientSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientSerializers, self).to_representation(instance)

        ret['state_name'] = StateSerializers(instance.state).data["state_name"]
        ret['city_name'] = CitySerializers(instance.city).data["city_name"]
        return ret

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone = data.get("phone")
        data["email"] = phone
        data["username"] = phone
        data["user_type"] = "PATIENT"
        passcode = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        data["password"] = passcode
        return data

    patient_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PatientModel
        fields = ['patient_id', 'first_name', 'last_name', 'middle_name', 'phone', 'state',
                  'city', 'married', 'department', 'patient_type', 'patient_detail', 'date_of_opd', 'registered_no',
                  'grand_parent_name', 'age', 'taluka', 'district', 'created_by', 'deleted']
