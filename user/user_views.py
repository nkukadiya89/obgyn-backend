from django.contrib.auth.models import Permission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from language.models import LanguageModel


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
        token.update({"userData": {'userName': self.user.username, 'userId': self.user.id,
                                   "defaultLanguageId": LanguageModel.objects.get(
                                       pk=self.user.default_language_id).language_id,
                                   "defaultLanguage": LanguageModel.objects.get(pk=self.user.default_language_id).code,
                                   "user_type": self.user.user_type, "permission": permission_list,
                                   "rs_per_visit": self.user.rs_per_visit,"rs_per_usg": self.user.rs_per_usg,
                                   "rs_per_room": self.user.rs_per_room,"operative_charge": self.user.operative_charge,
                                   "rs_per_day_nursing": self.user.rs_per_day_nursing,
                                   }})
        token.update()
        data["success"] = True
        data["msg"] = "Login Successful"
        data["data"] = token
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
