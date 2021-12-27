from django.db.models import Q
from rest_framework import serializers

from user.models import User


class UserSerializers(serializers.ModelSerializer):

    def validate(self, data):

        user_type = data.get('userType')

        if user_type == "DOCTOR" or user_type == "STAFF":

            # CHECK DUPLICATE AADHAR CARD NO
            aadhar_card = data.get('aadharCard')

            if len(aadhar_card) != 12 or not aadhar_card.isnumeric():
                raise serializers.ValidationError("Please enter a valid UID number.")

            duplicate_aadhar = User.objects.filter((Q(userType="DOCTOR") | Q(userType="STAFF")),
                                                   aadharCard__iexact=aadhar_card)

            if self.partial:
                duplicate_aadhar = duplicate_aadhar.filter(~Q(id=self.instance.id)).first()
            else:
                duplicate_aadhar = duplicate_aadhar.first()

            if duplicate_aadhar != None:
                raise serializers.ValidationError("UID number already exists! Please try with another aadhar number.")

            # CHECK IF SELECTED FOREIGN KEY IS OF HOSPITAL OR NOT
            hospital = data.get('hospital')
            if hospital:
                if hospital.userType != "HOSPITAL":
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

    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    username = serializers.CharField(required=False)
    userCode = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'firstName', 'lastName', 'middleName', 'password', 'userType', 'hospitalName',
                  'phone', 'state', 'city', 'area', 'pincode', 'email', 'landline', 'faxNumber', 'degree', 'speciality',
                  'aadharCard', 'registrationNo', 'defaultLanguage', 'designation', 'hospital', 'username', 'userCode',
                  'createdBy']
