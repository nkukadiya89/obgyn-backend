from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.response import Response


class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            raise

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

# class InvalidUser(AuthenticationFailed):
#     status_code = status.HTTP_406_NOT_ACCEPTABLE
#     default_detail = ("Credentials is invalid or didn't match")
#     default_code = 'user_credentials_not_valid'



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = {}
        token = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        token.update({"userData": {'userName': self.user.username, 'userId': self.user.id}})
        token.update()
        data["success"] = True
        data["msg"] = "Login Successful"
        data["data"] = token
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
