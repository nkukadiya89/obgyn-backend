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
    hospital = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False, required=False)

    def validate(self, data):

        user_type = data.get('user_type')

        if user_type == "DOCTOR" or user_type == "STAFF":

            # CHECK DUPLICATE AADHAR CARD NO
            aadhar_card = data.get('aadhar_card')

            if len(aadhar_card) != 12 or not aadhar_card.isnumeric():
                raise serializers.ValidationError("Please enter a valid UID number.")

            if user_type == "DOCTOR":
                duplicate_aadhar = User.objects.filter(user_type="DOCTOR", aadhar_card=aadhar_card).first()
            elif user_type == "STAFF":
                duplicate_aadhar = User.objects.filter(user_type="STAFF", aadhar_card=aadhar_card).first()

            if duplicate_aadhar != None:
                raise serializers.ValidationError("UID number already exists! Please try with another aadhar number.")

            # CHECK IF SELECTED FOREIGN KEY IS OF HOSPITAL OR NOT
            hospital = data.get('hospital')
            if hospital:
                if hospital.user_type != "HOSPITAL":
                    raise serializers.ValidationError("Please select hospital.")
            else:
                raise serializers.ValidationError("Please select hospital.")

            email = data.get('email')
            data["username"] = email
        elif user_type == "HOSPITAL":
            pass
        return data

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'password', 'user_type', 'hospital_name',
                  'phone', 'state',
                  'city', 'area', 'pincode', 'email', 'landline', 'fax_number', 'degree', 'speciality',
                  'aadhar_card', 'registration_no', 'default_language', 'designation', 'hospital']
