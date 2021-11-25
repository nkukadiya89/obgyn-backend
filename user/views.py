from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializers


# Create your views here.

@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        user = User()

        serializer = UserSerializers(user, data=request.data)

        data = {}
        if serializer.is_valid():

            new_user = serializer.save()
            user.set_password(request.data["password"])
            user.save()
            data['response'] = "successfully register a new user."
            data['email'] = new_user.email
        else:
            data = serializer.errors
        return Response(data)
