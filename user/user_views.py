from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = {}
        token = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        token.update({"userData": {'userName': self.user.username, 'userId': self.user.id,
                                   "defaultLanguageId": self.user.default_language_id}})
        token.update()
        data["success"] = True
        data["msg"] = "Login Successful"
        data["data"] = token
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
