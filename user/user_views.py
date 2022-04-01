from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from language.models import LanguageModel


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        attrs['email'] = attrs.get('email').lower()
        data = {}
        token = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        token.update({"userData": {'userName': self.user.username, 'userId': self.user.id,
                                   "defaultLanguageId": LanguageModel.objects.get(
                                       pk=self.user.default_language_id).language_id,
                                   "defaultLanguage": LanguageModel.objects.get(pk=self.user.default_language_id).code,
                                   "user_type": self.user.user_type}})
        token.update()
        data["success"] = True
        data["msg"] = "Login Successful"
        data["data"] = token
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
