import random
import string

from django.db.models.query import Q
from rest_framework import serializers

from city.serializers import CitySerializers
from state.serializers import StateSerializers
from .models import PatientModel
from manage_fields.serializers import ManageFieldsSerializers
from taluka.serializers import TalukaSerializers
from district.serializers import DistrictSerializers


class PatientSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(PatientSerializers, self).to_representation(instance)
        ret['state_name'] = StateSerializers(instance.state).data["state_name"]
        ret['city_name'] = CitySerializers(instance.city).data["city_name"]
        ret['name_title_name'] = ManageFieldsSerializers(instance.name_title).data["field_value"]
        ret['husband_title_name'] = ManageFieldsSerializers(instance.husband_title).data["field_value"]
        ret['grand_title_name'] = ManageFieldsSerializers(instance.grand_title).data["field_value"]
        ret['taluka_name'] = TalukaSerializers(instance.taluka).data["taluka_name"]
        ret["district_name"] = DistrictSerializers(instance.district).data["district_name"]
        return ret

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if "phone" in data:
            phone = data.get("phone")
            # user = User.objects.filter(email=phone)
            #
            # if self.partial:
            #     user = user.filter(~Q(pk=user[0].id)).first()
            # else:
            #     user = user.first()
            #
            # if user != None:
            #     first_name = user.first_name
            #     last_name = user.last_name
            #     middle_name = user.middle_name
            #     name = first_name + " " + middle_name + " " + last_name
            #     raise serializers.ValidationError(f'{phone} belongs to {name}. Provide alternative Contact number.')

            data["email"] = first_name[:2] + last_name[:2] + phone + "@yopmail.com"
            data["username"] = first_name[:2] + last_name[:2] + phone
        else:
            raise serializers.ValidationError("Phone is required.")

        user = PatientModel.objects.filter(
            Q(phone=data["phone"]) |
            Q(email=data["email"])
        )

        if self.partial:
            user = user.filter(~Q(pk=self.instance.patient_id)).first()
        else:
            user = user.first()


        if user != None:
            first_name = user.first_name
            last_name = user.last_name
            middle_name = user.middle_name
            regd_no = user.registered_no
            name = first_name + " " + middle_name + " " + last_name
            raise serializers.ValidationError(f"Patient {name} registered previously. Reg. No. {regd_no}")

        data["user_type"] = "PATIENT"
        passcode = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        data["password"] = passcode
        return data

    patient_id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    married = serializers.BooleanField(required=True)
    patient_type = serializers.CharField(required=True)
    patient_detail = serializers.CharField(required=True)
    department = serializers.CharField(required=True)
    date_of_opd = serializers.CharField(required=True)
    registered_no = serializers.CharField(read_only=True)
    profile_image = serializers.CharField(read_only=True)

    class Meta:
        model = PatientModel
        fields = ['patient_id', 'first_name', 'last_name', 'middle_name','name_title', 'phone', 'state',
                  'city', 'married', 'department', 'patient_type', 'patient_detail', 'date_of_opd', 'registered_no',
                  'grand_father_name','grand_title', 'husband_father_name','husband_title', 'age', 'taluka', 'district', 'created_by', 'deleted',
                  'hospital', 'profile_image']
        extra_kwargs = {
            "city": {"required": True},
            "state": {"required": True},
            "hospital": {"required": True},
        }
