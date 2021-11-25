from rest_framework import serializers

from city.models import CityModel
from language.models import LanguageModel
from state.models import StateModel
from user.models import User


class UserSerializers(serializers.ModelSerializer):
    state = serializers.PrimaryKeyRelatedField(queryset=StateModel.objects.all(), many=False, required=False)
    city = serializers.PrimaryKeyRelatedField(queryset=CityModel.objects.all(), many=False, required=False)
    default_language = serializers.PrimaryKeyRelatedField(queryset=LanguageModel.objects.all(), many=False,
                                                          required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'password', 'user_type', 'hospital_name', 'phone', 'state',
                  'city', 'area', 'pincode', 'email', 'landline', 'fax_number', 'degree', 'speciality',
                  'aadhar_card', 'registration_no', 'default_language', 'designation']
