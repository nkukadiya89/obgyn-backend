from django.db.models import Q
from rest_framework import serializers

from city.serializers import CitySerializers
from language.serializers import LanguageSerializers
from state.serializers import StateSerializers
from user.models import User


class DynamicFieldModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldModelSerializer, self).__init__(*args, **kwargs)

        fields = set(fields.split(","))

        if fields is not None:
            allowed = fields
            existing = set(self.fields)

            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def to_representation(self, instance,*args,**kwargs):
        ret = super(DynamicFieldModelSerializer, self).to_representation(instance)

        if instance.user_type == "HOSPITAL":
            if "first_name" in ret: ret.pop('first_name')
            if "last_name" in ret: ret.pop('last_name')
            if "middle_name" in ret: ret.pop('middle_name')

        if "state" in ret: ret['state_name'] = StateSerializers(instance.state).data["state_name"]
        if "city" in ret: ret['city_name'] = CitySerializers(instance.city).data["city_name"]
        if "default_language" in ret: ret['default_language_name'] = LanguageSerializers(instance.default_language).data[
            "language"]
        if "hospital" in ret: ret['hospitalname'] = UserSerializers(instance.hospital).data["hospital_name"]
        return ret

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'user_type', 'hospital_name',
                  'phone', 'state', 'city', 'area', 'pincode', 'email', 'landline', 'fax_number', 'degree',
                  'speciality', 'aadhar_card', 'registration_no', 'default_language', 'designation', 'hospital',
                  'username',
                  'user_code', 'created_by']


class UserSerializers(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(UserSerializers, self).to_representation(instance)
        ret.pop('password')

        if instance.user_type == "HOSPITAL":
            ret.pop('first_name')
            ret.pop('last_name')
            ret.pop('middle_name')

        ret['state_name'] = StateSerializers(instance.state).data["state_name"]
        ret['city_name'] = CitySerializers(instance.city).data["city_name"]
        ret['default_language_name'] = LanguageSerializers(instance.default_language).data["language"]
        ret['hospitalname'] = UserSerializers(instance.hospital).data["hospital_name"]
        return ret

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

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    user_code = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'middle_name', 'password', 'user_type', 'hospital_name',
                  'phone', 'state', 'city', 'area', 'pincode', 'email', 'landline', 'fax_number', 'degree',
                  'speciality',
                  'aadhar_card', 'registration_no', 'default_language', 'designation', 'hospital', 'username',
                  'user_code',
                  'created_by']
