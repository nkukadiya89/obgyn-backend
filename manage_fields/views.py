from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import ManageFieldsModel
from .serializers import ManageFieldsSerializers


class ManageFieldsAPI(APIView):
    # authentication_classes = (JWTTokenUserAuthentication,)
    # permission_classes = [IsAuthenticated]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        try:
            if id:
                manage_fields = ManageFieldsModel.objects.filter(pk=id)
            else:
                manage_fields = ManageFieldsModel.objects.all()
        except ManageFieldsModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serilizer = ManageFieldsSerializers(manage_fields, many=True)
            return Response(serilizer.data)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        try:
            manage_fields = ManageFieldsModel.objects.filter(pk=id).first()
        except ManageFieldsModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = ManageFieldsSerializers(manage_fields, request.data)
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
                manage_fields = ManageFieldsModel.objects.get(pk=id)
            else:
                manage_fields = ManageFieldsModel.objects.all()
        except ManageFieldsModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PATCH":
            serializer = ManageFieldsSerializers(manage_fields, request.data, partial=True)

            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "Update successfully"
                data["data"] = serializer.data
                return Response(data=data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ================= Delete Record =========================
    def delete(self, request, id):
        try:
            manage_fields = ManageFieldsModel.objects.get(pk=id)
        except ManageFieldsModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            manage_fields.deleted = 1
            manage_fields.save()
            data = {}
            data["success"] = "Delete successfull"

            return Response(data=data)

    # ================= Create New Record=========================
    def post(self, request):
        if request.method == "POST":
            manage_fields = ManageFieldsModel()
            serializer = ManageFieldsSerializers(manage_fields, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
