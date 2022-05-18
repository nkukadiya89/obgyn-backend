from django.contrib.auth.models import Permission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.timezone import now
from language.models import LanguageModel
from obgyn_config.models import ObgynConfigModel
from obgyn_config.views import get_obgyn_config


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        attrs['email'] = attrs.get('email').lower()
        data = {}
        token = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        group_permission = Permission.objects.filter(group__user=self.user)
        permission_list = {}
        for permission in group_permission:
            if permission.content_type.app_label in permission_list:
                permission_name = permission_list[permission.content_type.app_label]
                permission_list[permission.content_type.app_label] = ",".join(
                    [permission_name, permission.name.split(" ")[1]])
            else:
                permission_list[permission.content_type.app_label] = permission.name.split(" ")[1]
        
        obgyn_config = ObgynConfigModel.objects.filter(user_id=self.user.id).first()
        if obgyn_config == None:
            rs_per_visit=rs_per_usg=rs_per_room=operative_charge=rs_per_day_nursing=0
            monthly_usg=yearly_usg=1
        else:
            monthly_usg, yearly_usg = get_obgyn_config(self.user)
            rs_per_visit=obgyn_config.rs_per_visit
            rs_per_usg=obgyn_config.rs_per_usg
            rs_per_room=obgyn_config.rs_per_room
            operative_charge=obgyn_config.operative_charge
            rs_per_day_nursing=obgyn_config.rs_per_day_nursing
            monthly_usg=monthly_usg
            yearly_usg=yearly_usg

        token.update({"userData": {'userName': self.user.username, 'userId': self.user.id,
                                   "defaultLanguageId": LanguageModel.objects.get(
                                       pk=self.user.default_language_id).language_id,
                                   "defaultLanguage": LanguageModel.objects.get(pk=self.user.default_language_id).code,
                                   "hospital_id":self.user.hospital_id,
                                   "user_type": self.user.user_type, "permission": permission_list,
                                   "rs_per_visit": rs_per_visit,"rs_per_usg": rs_per_usg,
                                   "rs_per_room": rs_per_room,"operative_charge": operative_charge,
                                   "rs_per_day_nursing": rs_per_day_nursing,"monthly_usg": monthly_usg,
                                   "yearly_usg": yearly_usg,
                                   }})
        token.update()
        data["success"] = True
        data["msg"] = "Login Successful"
        data["data"] = token
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer



def generate_regd_no():
    return str(now()).replace("-", "").replace(":", "").replace(" ", "").replace(".", "").split("+")[0][:16]