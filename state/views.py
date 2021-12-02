from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import StateModel
from .serializers import StateSerializers


class StateAPI(APIView):
    # authentication_classes = (JWTTokenUserAuthentication,)
    # permission_classes = [IsAuthenticated]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        try:
            if id:
                state = StateModel.objects.filter(pk=id)
            else:
                state = StateModel.objects.all()
        except StateModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serilizer = StateSerializers(state, many=True)
            return Response(serilizer.data)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        try:
            state = StateModel.objects.filter(pk=id).first()
        except StateModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = StateSerializers(state, request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "Update successfully"
                data["data"] = serializer.data
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Partial Update of a record  =========================
    def patch(self, request, id):
        try:
            if id:
                state = StateModel.objects.get(state_id=id)
            else:
                state = StateModel.objects.all()
        except StateModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PATCH":
            serializer = StateSerializers(state, request.data, partial=True)

            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "Update successfully"
                data["data"]=serializer.data
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Delete Record =========================
    def delete(self, request, id):
        try:
            state = StateModel.objects.get(pk=id)
        except StateModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            state.deleted = 1
            state.save()
            data = {}
            data["success"] = "Delete successfull"

            return Response(data=data)

    # ================= Create New Record=========================
    def post(self, request):
        if request.method == "POST":
            state = StateModel()
            serializer = StateSerializers(state, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
