from django.db.models import Q
from rest_framework import serializers

from user.models import User


class UserSerializers(serializers.ModelSerializer):

    def validate(self, data):

        user_type = data.get('user_type')

        if user_type == "DOCTOR" or user_type == "STAFF":

            # CHECK DUPLICATE AADHAR CARD NO
            aadhar_card = data.get('aadhar_card')

            if len(aadhar_card) != 12 or not aadhar_card.isnumeric():
                raise serializers.ValidationError("Please enter a valid UID number.")

            duplicate_aadhar = User.objects.filter((Q(user_type="DOCTOR") | Q(user_type="STAFF")),
                                                   aadhar_card__iexact=aadhar_card)

            if self.partial:
                duplicate_aadhar = duplicate_aadhar.filter(~Q(id=self.instance.id)).first()
            else:
                duplicate_aadhar = duplicate_aadhar.first()

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
            username = data.get("username")
            duplicate_username = User.objects.filter(username=username)
            if self.partial:
                duplicate_username = duplicate_username.filter(~Q(id=self.instance.id)).first()
            else:
                duplicate_username = duplicate_username.first()

            if duplicate_username != None:
                raise serializers.ValidationError("Username already taken.")

        return data

    firstName = serializers.CharField(source='first_name', required=False)
    lastName = serializers.CharField(source='last_name', required=False)
    middleName = serializers.CharField(source='middle_name', required=False)
    userType = serializers.CharField(source='user_type')
    hospitalName = serializers.CharField(source='hospital_name', required=False)
    faxNumber = serializers.CharField(source='fax_number', required=False)
    aadharCard = serializers.CharField(source='aadhar_card', required=False)
    registrationNo = serializers.CharField(source='registration_no', required=False)
    defaultLanguage = serializers.IntegerField(source='default_language_id', required=False)
    username = serializers.CharField(required=False)
    createdBy = serializers.IntegerField(source='created_by')

    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'middleName', 'password', 'userType', 'hospitalName',
                  'phone', 'state', 'city', 'area', 'pincode', 'email', 'landline', 'faxNumber', 'degree', 'speciality',
                  'aadharCard', 'registrationNo', 'defaultLanguage', 'designation', 'hospital', 'username', 'createdBy']

