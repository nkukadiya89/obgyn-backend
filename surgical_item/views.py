from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import SurgicalItemModel,SurgicalItemGroupModel
from .serializers import SurgicalItemSerializers, SurgicalItemGroupSerializers


class SurgicalItemAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        try:
            if id:
                surgical_item = SurgicalItemModel.objects.filter(pk=id)
            else:
                surgical_item = SurgicalItemModel.objects.all()
        except SurgicalItemModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serilizer = SurgicalItemSerializers(surgical_item, many=True)
            return Response(serilizer.data)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        try:
            surgical_item = SurgicalItemModel.objects.filter(pk=id).first()
        except SurgicalItemModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = SurgicalItemSerializers(surgical_item, request.data)
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
                surgical_item = SurgicalItemModel.objects.get(surgical_item_id=id)
            else:
                surgical_item = SurgicalItemModel.objects.all()
        except SurgicalItemModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PATCH":
            serializer = SurgicalItemSerializers(surgical_item, request.data, partial=True)

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
            surgical_item = SurgicalItemModel.objects.get(pk=id)
        except SurgicalItemModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            surgical_item.deleted = 1
            surgical_item.save()
            data = {}
            data["success"] = "Delete successfull"

            return Response(data=data)

    # ================= Create New Record=========================
    def post(self, request):
        if request.method == "POST":
            surgical_item = SurgicalItemModel()
            serializer = SurgicalItemSerializers(surgical_item, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SurgicalItemGroupAPI(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = [IsAuthenticated]

    # ================= Retrieve Single or Multiple records=========================
    def get(self, request, id=None):
        try:
            if id:
                surgical_item_group = SurgicalItemGroupModel.objects.filter(pk=id)
            else:
                surgical_item_group = SurgicalItemGroupModel.objects.all()
        except SurgicalItemGroupModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            serilizer = SurgicalItemGroupSerializers(surgical_item_group, many=True)
            return Response(serilizer.data)

    # ================= Update all Fields of a record =========================
    def put(self, request, id):
        try:
            surgical_item_group = SurgicalItemGroupModel.objects.filter(pk=id).first()
        except SurgicalItemGroupModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PUT":
            serializer = SurgicalItemGroupSerializers(surgical_item_group, request.data)
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
                surgical_item_group = SurgicalItemGroupModel.objects.get(si_group_id=id)
            else:
                surgical_item_group = SurgicalItemGroupModel.objects.all()
        except SurgicalItemGroupModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "PATCH":
            serializer = SurgicalItemGroupSerializers(surgical_item_group, request.data, partial=True)

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
            surgical_item_group = SurgicalItemGroupModel.objects.get(pk=id)
        except SurgicalItemGroupModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "DELETE":
            surgical_item_group.deleted = 1
            surgical_item_group.save()
            data = {}
            data["success"] = "Delete successfull"

            return Response(data=data)

    # ================= Create New Record=========================
    def post(self, request):
        if request.method == "POST":
            surgical_item_group = SurgicalItemGroupModel()
            serializer = SurgicalItemGroupSerializers(surgical_item_group, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
